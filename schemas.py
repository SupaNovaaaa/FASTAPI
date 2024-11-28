
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import ClassVar

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(BaseModel):
    pass

class Post(BaseModel):
        id:int
        created_at:datetime
        
        class Config:
            orm_mode=True

class UserCreate(BaseModel):
    email: EmailStr  
    password: str 

class UserOut(BaseModel):
     id:int
     email:EmailStr

     class Config:
            orm_mode=True


