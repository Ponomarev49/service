from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.article_model import Article
from src.models.user_model import User
from slugify import slugify


def create_article(db: Session, user_id: int, data: dict):
    slug = slugify(data["title"])
    if db.query(Article).filter(Article.slug == slug).first():
        raise HTTPException(status_code=400, detail="Article with this title already exists")

    article = Article(
        slug=slug,
        title=data["title"],
        description=data["description"],
        body=data["body"],
        tag_list=",".join(data.get("tagList", [])),
        author_id=user_id,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def list_articles(db: Session):
    return db.query(Article).all()


def get_article_by_slug(db: Session, slug: str):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


def update_article(db: Session, user_id: int, slug: str, data: dict):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this article")

    for field in ["title", "description", "body"]:
        if field in data and data[field] is not None:
            setattr(article, field, data[field])

    if "tagList" in data:
        article.tag_list = ",".join(data["tagList"])

    if "title" in data:
        article.slug = slugify(data["title"])

    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, user_id: int, slug: str):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this article")

    db.delete(article)
    db.commit()
    return {"detail": "Article deleted"}
