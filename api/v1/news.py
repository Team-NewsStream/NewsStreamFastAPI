from typing import List, Optional

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from db.base import get_db
from repositories.article import get_trending_articles, get_category_articles, get_all_categories
from schemas.news import ArticleResponse, CategoryResponse

router = APIRouter(tags=["News"], prefix="/v1")


@router.get(
    "/category-news/all",
    response_model=List[ArticleResponse],
    dependencies=[Depends(get_current_user)]
)
def fetch_unfiltered_news(
        db: Session = Depends(get_db),
        last_item_id: Optional[int] = None,
        page_size: int = 25
):
    """Protected route: Fetch all news, irrespective of category."""
    if page_size > 50:
        page_size = 50
    articles = get_category_articles(db=db, last_item_id=last_item_id, page_size=page_size)
    return articles


@router.get(
    "/category-news/{category}",
    response_model=List[ArticleResponse],
    dependencies=[Depends(get_current_user)]
)
def fetch_category_articles(
        category: str,
        last_item_id: int = None,
        page_size: int = 25,
        db: Session = Depends(get_db)
):
    """Protected route: Fetch category-wise news."""
    if page_size > 50:
        page_size = 50
    return get_category_articles(db, category=category, last_item_id=last_item_id, page_size=page_size)


@router.get(
    "/trending-topics",
    response_model=List[ArticleResponse],
    dependencies=[Depends(get_current_user)]
)
def fetch_trending_topics(
        page: int = 1,
        page_size: int = 25,
        db: Session = Depends(get_db)
):
    """Protected route: Fetch trending news."""
    if page_size > 50:
        page_size = 50
    articles = get_trending_articles(db=db, page=page, page_size=page_size)
    return [ArticleResponse.model_validate(article) for article in articles] if articles else []


@router.get(
    "/categories",
    response_model=List[CategoryResponse],
    dependencies=[Depends(get_current_user)]
)
def fetch_categories(db: Session = Depends(get_db)):
    """Protected route: Fetch all categories."""
    return get_all_categories(db=db)
