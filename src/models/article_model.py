from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from slugify import slugify  # pip install python-slugify


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    tag_list = Column(String, nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", backref="articles")
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")

    def generate_slug(self):
        self.slug = slugify(self.title)
