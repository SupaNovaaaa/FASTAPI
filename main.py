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
from passlib.context import CryptContext
from . import models, schemas
from app.utils import hash
from .database import engine, get_db
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

@app.get("/")
def root():
    return {"message": "Hello World!!!!"}



@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db)):
    #cursor.execute("""SELECT *FROM posts""")
    #posts =cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.Post,db:Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts(title,content, published) VALUES(%s, %s,%s) RETURNING*  """,(post.title,post.content,post.published))
    #new_post=cursor.fetchone()
    #conn.commit()
    ##new_post=models.Post(**post.dict())
    result = post.dict()

    for i in result.keys():
        print(f"{i}:{result[i]}")

    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int,db:Session = Depends(get_db)):
    #cursor.execute("""SELECT *FROM posts WHERE id =%s""",(str(id),))
    #post = cursor.fetchone()
    #
    #
    post =db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"post with id:{id} was not found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING*""",(str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post =db.query(models.Post).filter(models.Post.id==id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int,updated_post: schemas.Post,db:Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title =%s,content=%s,published=%s WHERE id = %s RETURNING*""",(post.title,post.content,post.published,str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id==id)

    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with id:{id} does not exist")
    
    post_query.update(updated_post.dict(),synchronize_session=False)

    db.commit()
    return  post_query.first()

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    
    #hash the password - user.password
    
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

