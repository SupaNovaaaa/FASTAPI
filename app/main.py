from typing import Optional,List
from fastapi import FastAPI,Response, status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from sqlalchemy.sql.functions import mode
from . import models, schemas,utils
from .database import engine, get_db
from .routers import post,users,auth,vote

from passlib.context import CryptContext
from .config import settings






#from app.schemas import UserCreate


#from . import models,schemas
from app import schemas
from app import models
#from app import models, schemas
def some_function():
    from app.schemas import UserCreate

from .database import engine,SessionLocal

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
models.Base.metadata.create_all(bind=engine)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(BaseModel):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



app = FastAPI()


    



while True:

    try:
        conn= psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='lol',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(2)


my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favourite foods","content":"I like pizza","id":2}]
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
def root():
    return {"message": "Hello World!!!!"}



