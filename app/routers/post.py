from .. import models,schemas,oauth2
from fastapi import FastAPI,Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import  get_db
from typing import List,Optional


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), limit: int = 3, skip: int = 0 , search: Optional[str]=""):
    #cursor.execute("""SELECT *FROM posts""")
    #posts =cursor.fetchall()
    print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts(title,content, published) VALUES(%s, %s,%s) RETURNING*  """,(post.title,post.content,post.published))
    #new_post=cursor.fetchone()
    #conn.commit()
    ##new_post=models.Post(**post.dict())
    result = post.dict()

    for i in result.keys():
        print(f"{i}:{result[i]}")

    new_post=models.Post(owner_id=current_user.id,**result)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT *FROM posts WHERE id =%s""",(str(id),))
    #post = cursor.fetchone() 
    #
    #
    post =db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"post with id:{id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING*""",(str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query =db.query(models.Post).filter(models.Post.id==id)

    post = post_query.fist()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    
    if post.owner.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorised to perform reaquested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Retrieve the post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if post.owner.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorised to perform reaquested action")

    # Update the post
    post_query.update(
        {
            models.Post.title: updated_post.title,
            models.Post.content: updated_post.content,
            models.Post.published: updated_post.published
        },
        synchronize_session=False
    )
    db.commit()
    return post_query.first()
