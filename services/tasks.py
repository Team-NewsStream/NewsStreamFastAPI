import asyncio
from typing import List

import httpx
from celery.utils.log import get_task_logger
from sqlalchemy.orm import Session

from core.settings import settings
from db.base import get_db
from repositories import article
from services import cloud_run_auth
from services.celery_config import celery_app
from utils.utils import retrieve_news_content

logger = get_task_logger(__name__)


async def trigger_scraper(
        last_item_uuid: str = None,
        limit: int = 25,
):
    async with httpx.AsyncClient() as client:
        auth_token = cloud_run_auth.get_cloud_run_id_token(
            settings.SCRAPER_SERVICE_URL
        )
        logger.info("Successfully authenticated with scraper service. Fetching news...")
        headers = {"Authorization": f"Bearer {auth_token}"}
        params = {"last_item_uuid": last_item_uuid, "limit": limit}
        url = f"{settings.SCRAPER_SERVICE_URL}/fetch_news"
        response = await client.get(
            headers=headers,
            url=url,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()


async def trigger_ml_inference(data: dict[str, List[str]]):
    async with httpx.AsyncClient() as client:
        auth_token = cloud_run_auth.get_cloud_run_id_token(
            settings.ML_INFERENCE_SERVICE_URL
        )
        logger.info("Successfully authenticated with ML inference service. Predicting...")
        headers = {"Authorization": f"Bearer {auth_token}"}
        url = f"{settings.ML_INFERENCE_SERVICE_URL}/predict"
        response = await client.post(
            headers=headers,
            url=url,
            json=data,
            timeout=180
        )
        response.raise_for_status()
        return response.json()


@celery_app.task(bind=True)
def fetch_and_save_news(self):
    """
    Celery task to fetch news and process through ML.
    """
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        last_item_uuid = article.get_last_item_uuid(db=db)
        logger.info(f"Starting process with last_item_uuid: {last_item_uuid}")

        news_data = asyncio.run(trigger_scraper(last_item_uuid=last_item_uuid))
        if not news_data:
            logger.info("No new news to process.")
            return {"status": "success", "processed": 0}

        titles = [item["title"] for item in news_data if "title" in item]

        ml_results = asyncio.run(trigger_ml_inference({"texts": titles}))

        article_creates, categories_set, sources_map = retrieve_news_content(
            news_data=news_data,
            ml_data=ml_results
        )

        logger.info(f"Successfully processed {len(article_creates)} articles. Inserting into database...")

        db_articles = article.create_articles(
            db=db,
            article_creates=article_creates,
            categories_set=categories_set,
            sources_map=sources_map
        )
        articles_count = len(db_articles)
        logger.info(f"Successfully inserted {len(db_articles)} articles")
        return {"status": "success", "processed": articles_count}

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching news: {str(e)}")
        db.rollback()
        self.retry(exc=e, countdown=30 * self.request.retries)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        db.rollback()
        self.retry(exc=e, countdown=60 * self.request.retries)
    finally:
        next(db_gen, None)
