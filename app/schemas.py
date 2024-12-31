from typing_extensions import Annotated
from datetime import datetime
from pydantic import BaseModel, EmailStr, conint, Field
from typing import ClassVar,Optional

ConstrainedInt = conint(le=1)


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    created_at: Optional[datetime] = None

# Schema for creating a post, excludes id
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
     id:int
     email:EmailStr

     class Config:
            orm_mode=True

# Schema for representing a post with an optional id
class Post(PostBase):
    id: Optional[int] = None
    owner_id: Optional[int] = None
    owner: UserOut
    
    class Config:
         orm_mode=True 


class PostOut(BaseModel):
     Post: Post
     votes: Optional[int]

     class Config:
          orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr  
    password: str 


class UserLogin(BaseModel):
     email: str
     password: str

class Token(BaseModel):
     access_token: str
     token_type: str

class TokenData(BaseModel):
     id: Optional[int] = None

class Vote(BaseModel):
     post_id: int 
     dir:Annotated[int, Field(strict=True, ge=0, le =1)]
