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
    comments = relationship("Comment", back_populates="author")

class Post(Base):
    __tablename__= "posts"

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String, nullable = False)
    content = Column(Text, nullable = False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"),nullable =False)

    author=relationship("User", back_populates = "posts")
    comments = relationship("Comment", back_populates = "post",
                            cascade="all, delete-orphan")

class Comment(Base):
    __tablename__="comments"

    id = Column(Integer,primary_key=True,index=True)
    content = Column(Text, nullable = False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable = False)

    author = relationship("User", back_populates = "comments")
    post = relationship("Post", back_populates = "comments")