from pydantic import BaseModel
from typing import List, Optional


class ArticleBase(BaseModel):
    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = None


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    pass


class ArticleResponse(ArticleBase):
    slug: str
    id: int
    author_id: int

    class Config:
        from_attributes = True
