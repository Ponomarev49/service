from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.comment_model import Comment
from src.models.article_model import Article


def add_comment(db: Session, slug: str, body: str, user_id: int):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    comment = Comment(body=body, article_id=article.id, author_id=user_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments(db: Session, slug: str):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return db.query(Comment).filter(Comment.article_id == article.id).all()


def delete_comment(db: Session, slug: str, comment_id: int, user_id: int):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # (опционально) проверка, что пользователь — автор
    if comment.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this comment")

    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}
