from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):

    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    
    access_token: str
    token_type: str

class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length =1)

class AuthorResponse(BaseModel):

    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    user_id: int
    author: AuthorResponse

    class Config:
        from_attributes = True