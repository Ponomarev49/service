from pydantic import BaseModel
from typing import Optional


class CommentBase(BaseModel):
    body: str


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    author_id: Optional[int]

    class Config:
        orm_mode = True
