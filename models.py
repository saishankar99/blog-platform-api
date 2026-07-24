from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default = func.now())

    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__= "posts"

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String, nullable = False)
    content = Column(Text, nullable = False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"),nullable =False)

    author=relationship("User", back_populates = "posts")


