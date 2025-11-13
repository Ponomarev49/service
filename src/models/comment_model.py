from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(String, nullable=False)

    # Внешний ключ на статью
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))

    # Внешний ключ на автора (если есть модель User)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    # Отношения
    article = relationship("Article", back_populates="comments")
    author = relationship("User", back_populates="comments", lazy="joined")
