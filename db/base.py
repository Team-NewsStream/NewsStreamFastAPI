from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.settings import settings

SQLALCHEMY_DATABASE_URL = settings.DB_URL

pool = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=3,
    max_overflow=2,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pool)

Base = declarative_base()


# Dependency to get a session
def get_db():
    """
    Dependency to get a db session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
