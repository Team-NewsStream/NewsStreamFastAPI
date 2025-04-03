from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from db.base import get_db
from repositories.article import get_trending_articles, get_category_articles, get_all_categories
from schemas.news import ArticleResponse, CategoryResponse

router = APIRouter(tags=["News"])


@router.get("/category-news/{category}", response_model=List[ArticleResponse])
def fetch_category_articles(
        category: str,
        last_item_id: int,
        page_size: int = 25,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)  # 🔒 Requires Authentication
):
    """Protected route: Fetch category-wise news."""
    return get_category_articles(db, category=category, last_item_id=last_item_id, page_size=page_size)


@router.get("/trending-topics", response_model=List[ArticleResponse])
def fetch_trending_topics(
        page: int = 1,
        page_size: int = 25,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)  # 🔒 Requires Authentication
):
    """Protected route: Fetch trending news."""
    return get_trending_articles(db=db, page=page, page_size=page_size)


@router.get("/category-news/all", response_model=List[ArticleResponse])
def fetch_unfiltered_news(
        db: Session = Depends(get_db),
        last_item_id: int = 0,
        page_size: int = 25,
        user=Depends(get_current_user)  # 🔒 Requires Authentication
):
    """Protected route: Fetch all news, irrespective of category."""
    return get_category_articles(db=db, last_item_id=last_item_id, page_size=page_size)


@router.get("/categories", response_model=List[CategoryResponse])
def fetch_categories(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Protected route: Fetch all categories."""
    return get_all_categories(db=db)
