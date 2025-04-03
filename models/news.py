from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.base import Base


class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    source_image_url = Column(String)

    articles = relationship('Article', back_populates='source')


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    articles = relationship('Article', back_populates='category')


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    url_to_image = Column(String, nullable=True)
    published_at = Column(DateTime, index=True, default=datetime.now(timezone.utc), nullable=False)
    sentiment = Column(String, nullable=False)  # Positive, Negative

    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    source = relationship('Source', back_populates='articles')
    category = relationship('Category', back_populates='articles')


class Trending(Base):
    __tablename__ = 'trending'

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
