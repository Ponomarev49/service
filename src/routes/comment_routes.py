from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.schemas.comment_schema import CommentCreate, CommentResponse
from src.controllers.comment_controller import add_comment, get_comments, delete_comment
from typing import List

router = APIRouter(prefix="/api/articles", tags=["comments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# POST /api/articles/{slug}/comments
@router.post("/{slug}/comments", response_model=CommentResponse)
def create_comment(slug: str, comment: CommentCreate, db: Session = Depends(get_db), user_id: int = 1):
    # user_id=1 временно — потом добавим JWT
    return add_comment(db, slug, comment.body, user_id)


# GET /api/articles/{slug}/comments
@router.get("/{slug}/comments", response_model=List[CommentResponse])
def read_comments(slug: str, db: Session = Depends(get_db)):
    return get_comments(db, slug)


# DELETE /api/articles/{slug}/comments/{id}
@router.delete("/{slug}/comments/{id}")
def remove_comment(slug: str, id: int, db: Session = Depends(get_db), user_id: int = 1):
    return delete_comment(db, slug, id, user_id)
