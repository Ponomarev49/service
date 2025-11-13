from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.database import SessionLocal
from src.controllers import article_controller, user_controller
from src.schemas.article_schema import ArticleCreate, ArticleUpdate, ArticleResponse

router = APIRouter(prefix="/api/articles", tags=["Articles"])
bearer_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=ArticleResponse)
def create_article(
    article: ArticleCreate,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user = user_controller.get_current_user(db, token)
    return article_controller.create_article(db, user.id, article.model_dump())


@router.get("", response_model=list[ArticleResponse])
def list_articles(db: Session = Depends(get_db)):
    return article_controller.list_articles(db)


@router.get("/{slug}", response_model=ArticleResponse)
def get_article(slug: str, db: Session = Depends(get_db)):
    return article_controller.get_article_by_slug(db, slug)


@router.put("/{slug}", response_model=ArticleResponse)
def update_article(
    slug: str,
    article: ArticleUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user = user_controller.get_current_user(db, token)
    return article_controller.update_article(db, user.id, slug, article.model_dump())


@router.delete("/{slug}")
def delete_article(
    slug: str,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user = user_controller.get_current_user(db, token)
    return article_controller.delete_article(db, user.id, slug)
