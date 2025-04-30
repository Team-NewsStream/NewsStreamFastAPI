from datetime import datetime
from typing import Dict, Any

from models.news import Article
from schemas.news import ArticleCreate, SourceCreate


def map_to_article_create(news_item: Dict[str, Any], ml_data: Dict[str, Any]):
    source_data = news_item.get("source", {})
    source = SourceCreate(
        name=source_data.get("name", ""),
        logo_url=source_data.get("logo_url", "")
    )

    published_at_raw = news_item.get("publishedAt")
    published_at = datetime.fromisoformat(published_at_raw) if isinstance(published_at_raw, str) else published_at_raw

    return ArticleCreate(
        uuid=news_item.get("uuid"),
        title=news_item.get("title", ""),
        url=news_item.get("url", ""),
        description=news_item.get("description"),
        url_to_image=news_item.get("urlToImage"),
        published_at=published_at,
        source=source,
        sentiment=ml_data.get("sentiment"),
        category=ml_data.get("category"),
        is_trending=news_item.get("isTrending")
    )


def article_create_to_article(
        article_create: ArticleCreate,
        category_id: int,
        source_id: int,
) -> Article:
    title = article_create.title[:500] if article_create.title else None
    description = article_create.description[:1000] if article_create.description else None
    return Article(
        uuid=article_create.uuid,
        title=title,
        url=article_create.url,
        description=description,
        url_to_image=article_create.url_to_image,
        published_at=article_create.published_at,
        sentiment=article_create.sentiment,
        source_id=source_id,
        category_id=category_id,
    )


def map_to_source_create(name: str, logo_url: str | None) -> SourceCreate:
    return SourceCreate(
        name=name,
        logo_url=logo_url
    )
