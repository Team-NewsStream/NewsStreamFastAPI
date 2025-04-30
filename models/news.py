from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from db.base import Base


class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), index=True)
    logo_url = Column(Text)

    articles = relationship('Article', back_populates='source')


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    articles = relationship('Article', back_populates='category')


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String(64), index=True, nullable=False)
    title = Column(String(512), nullable=False)
    url = Column(String(1024), nullable=False)
    description = Column(String(1024), nullable=True)
    url_to_image = Column(Text, nullable=True)
    published_at = Column(DateTime, index=True, default=datetime.now(timezone.utc), nullable=False)
    sentiment = Column(String(32), nullable=False)  # Positive, Negative

    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    source = relationship('Source', back_populates='articles')
    category = relationship('Category', back_populates='articles')


class Trending(Base):
    __tablename__ = 'trending'

    id = Column(Integer, primary_key=True, index=True)
    article_uuid = Column(String(64), ForeignKey("articles.uuid"), nullable=False)
