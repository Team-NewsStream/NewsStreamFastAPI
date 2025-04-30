from sqlalchemy import Column, String

from db.base import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String(255), primary_key=True, index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
