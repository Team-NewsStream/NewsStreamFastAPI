from typing import Optional, List

from sqlalchemy.orm import Session

from models.news import Article, Trending, Category, Source
from schemas.news import ArticleCreate, SourceCreate, CategoryCreate
from utils.mapper import article_create_to_article


def create_articles(
        db: Session,
        article_creates: List[ArticleCreate],
        categories_set: set[str],
        sources_map: dict[str, str]
):
    """
    Create articles, their categories, and sources, and store them in the database. Also, handle the
    creation of trending articles based on their properties, ensuring the relationships between
    categories, sources, and articles are correctly established and persisted.

    :param db: Database session object used for database operations.
    :type db: Session
    :param article_creates: List of article creation objects containing article data to be inserted
        into the database.
    :type article_creates: List[ArticleCreate]
    :param categories_set: Set of unique category names to create or retrieve from the database.
    :type categories_set: set[str]
    :param sources_map: Dictionary mapping source names to source URLs, defining sources for the
        articles to be created.
    :type sources_map: dict[str, str]
    :return: List of newly created article objects after being committed to the database.
    :rtype: List[Article]
    """
    db_categories = create_categories_from_names(db=db, names=categories_set)
    db_sources = create_sources_from_dict(db=db, sources=sources_map)

    category_name_to_id = {category.name: category.id for category in db_categories}
    source_name_to_id = {source.name: source.id for source in db_sources}

    db_articles = []
    trending_articles = []

    for article_in in article_creates:
        category_id = category_name_to_id.get(article_in.category)
        source_id = source_name_to_id.get(article_in.source.name)

        db_articles.append(article_create_to_article(article_in, category_id, source_id))

    db.add_all(db_articles)
    db.flush()
    for article_in in article_creates:
        if article_in.is_trending:
            trending_articles.append(Trending(article_uuid=article_in.uuid))

    db.add_all(trending_articles)
    db.commit()
    for article in db_articles:
        db.refresh(article)
    return db_articles


def get_category_articles(
        db: Session,
        last_item_id: int = None,
        category: Optional[str] = None,
        page_size: int = 25
) -> list[Article]:
    """Fetch articles, optionally filtered by category and paginated."""
    query = db.query(Article).order_by(Article.id.desc())

    if category is not None and category != "all":
        query = query.filter(Article.category.has(name=category))

    if last_item_id is not None:
        query = query.filter(Article.id < last_item_id)

    articles = query.limit(page_size).all()
    return articles if articles else []


def get_trending_articles(
        db: Session,
        last_item_id: Optional[int] = None,
        omit_negative_sentiment: bool = False,
        page_size: int = 25
) -> list[Article]:
    """Fetch trending articles, paginated."""
    query = (
        db.query(Article)
        .join(Trending, Article.uuid == Trending.article_uuid)
        .order_by(Article.id.desc())
    )

    if last_item_id is not None:
        query = query.filter(Article.id < last_item_id)

    if omit_negative_sentiment:
        query = query.filter(Article.sentiment == "positive")

    articles = query.limit(page_size).all()
    return articles if articles else []


def remove_trending_article(db: Session, article_uuid: str):
    """Remove an article from trending."""
    db.query(Trending).filter(article_uuid=article_uuid).delete()
    db.commit()


def create_category(db: Session, category_data: CategoryCreate) -> Category:
    """Insert a new category into the database."""
    db_category = Category(**category_data.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def create_categories_from_names(db: Session, names: set[str]):
    """
    Creates and persists new category entries in the database for names
    that do not yet exist and retrieves both existing and newly created
    categories.

    :param db: Database session object used for querying and persisting
        category entities.
    :type db: Session
    :param names: Set of category names to create or retrieve from the
        database.
    :type names: Set[str]
    :return: List of existing and newly created categories corresponding
        to the supplied category names.
    :rtype: list[Category]
    """
    existing_categories = get_categories_by_name(db, names=names)
    existing_names = set()
    if existing_categories is not None:
        existing_names = {category.name for category in existing_categories}

    missing_names = names - existing_names

    new_categories = [Category(name=name) for name in missing_names] if missing_names else []

    db.add_all(new_categories)
    db.flush()

    if existing_categories is not None:
        return existing_categories + new_categories

    return new_categories


def get_categories_by_name(db: Session, names: set[str]) -> Optional[List[Category]]:
    """Retrieve categories by their names."""
    categories = db.query(Category).filter(Category.name.in_(names)).all()
    return categories if categories else None


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


def create_sources_from_dict(db: Session, sources: dict[str, str]) -> List[Source]:
    """
    Create or retrieve sources from a dictionary of source names and their associated
    logo URLs.

    :param db: Session
        The SQLAlchemy database session used for querying and persisting sources.
    :param sources: Dict[str, str]
        A dictionary mapping source names to their respective logo URLs.
    :return: List[Source]
        A list of Source objects representing both existing and newly created sources.
    """
    sources_set = set(sources)
    existing_sources = get_sources_by_name(db, names=sources_set)

    existing_names = set()
    if existing_sources is not None:
        existing_names = {source.name for source in existing_sources}

    missing_names = sources_set - existing_names

    new_sources = [
        Source(name=name, logo_url=sources[name])
        for name in missing_names
    ] if missing_names else []

    db.add_all(new_sources)
    db.flush()

    if existing_sources is not None:
        return existing_sources + new_sources

    return new_sources


def get_sources_by_name(db: Session, names: set[str]) -> Optional[List[Source]]:
    """Retrieve a list of sources matching the given names."""
    sources = db.query(Source).filter(Source.name.in_(names)).all()
    return sources if sources else None


def get_last_item_uuid(db: Session):
    """Retrieve the ID of the last article in the database."""
    article = db.query(Article).order_by(Article.id.desc()).first()
    uuid = article.uuid if article else None
    return uuid
