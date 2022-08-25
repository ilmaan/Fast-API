import email
from optparse import Option
from pydantic import BaseModel, EmailStr 
from datetime import datetime
from typing import Optional


# class Post(BaseModel): 
#     title: str
#     content: str


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserCreate):
    id: int
    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

