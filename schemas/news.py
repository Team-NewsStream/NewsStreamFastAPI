from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SourceResponse(BaseModel):
    id: int
    name: str
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True


class SourceCreate(BaseModel):
    name: str
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ArticleResponse(BaseModel):
    id: int
    title: str
    url: str
    description: Optional[str] = None
    url_to_image: str = None
    published_at: datetime = None
    source: SourceResponse
    sentiment: str = None
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True


class ArticleCreate(BaseModel):
    uuid: str
    title: str
    url: str
    description: Optional[str] = None
    url_to_image: str
    published_at: datetime = None
    source: SourceCreate
    sentiment: str = None
    category: Optional[str] = None,
    is_trending: bool = False

    class Config:
        from_attributes = True
