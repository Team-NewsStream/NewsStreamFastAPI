from sqlalchemy import Column, String

from db.base import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
