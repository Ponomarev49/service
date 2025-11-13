from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    comments = relationship("Comment", back_populates="author")
