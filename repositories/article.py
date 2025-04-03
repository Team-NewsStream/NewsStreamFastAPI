from typing import Optional

from sqlalchemy.orm import Session

from models.news import Article, Trending, Category, Source
from schemas.news import ArticleCreate, SourceCreate, CategoryCreate


def create_article(db: Session, article: ArticleCreate):
    """Inserts a new Article into the database"""
    article = Article(**article.model_dump())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def get_category_articles(
        db: Session,
        last_item_id: int,
        category: Optional[str] = None,
        page_size: int = 25
):
    """Fetch articles, optionally filtered by category and paginated."""
    query = db.query(Article).order_by(Article.id.desc())

    if category is not None and category != 'all':
        query = query.filter(Article.category.has(name=category))

    return query.filter(Article.id < last_item_id).limit(page_size).all()


def get_trending_articles(db: Session, page: int = 1, page_size: int = 25):
    """Fetch trending articles, paginated."""
    query = (db.query(Article)
             .join(Trending, Article.id == Trending.article_id)
             .order_by(Article.id.desc()))
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all()


def mark_article_trending(db: Session, article_id: int) -> Trending:
    """Mark an article as trending."""
    db_trending = Trending(article_id=article_id)
    db.add(db_trending)
    db.commit()
    db.refresh(db_trending)
    return db_trending


def remove_trending_article(db: Session, article_id: int):
    """Remove an article from trending."""
    db.query(Trending).filter(article_id=article_id).delete()
    db.commit()


def create_category(db: Session, category_data: CategoryCreate) -> Category:
    """Insert a new category into the database."""
    db_category = Category(**category_data.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    """Retrieve a category by name."""
    return db.query(Category).filter(Category.name == name).first()


def get_all_categories(db: Session):
    """Retrieve all categories."""
    return db.query(Category).all()


def create_source(db: Session, source_data: SourceCreate) -> Source:
    """Insert a new news source into the database."""
    db_source = Source(**source_data.model_dump())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def get_source_by_name(db: Session, name: str) -> Optional[Source]:
    """Retrieve a source by name."""
    return db.query(Source).filter(Source.name == name).first()
