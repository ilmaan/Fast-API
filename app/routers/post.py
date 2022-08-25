from app import oauth2
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from ..database import get_db
from typing import List, Optional
import psycopg2 
from sqlalchemy.orm import Session 
from psycopg2.extras import RealDictCursor 
from datetime import time



router = APIRouter(
    prefix="/posts",
    tags=['posts']
) 

mposts = [{"id":1,"title":"title1","content":"content1"},{"id":2,"title":"title2","content":"content2"}]

@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    # return {"posts":posts}
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model= schemas.Post)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    print(post, type(post),'8'*100)
    # new_post = models.Post(title=post.title, content=post.content)
    new_post = models.Post(**post.dict())
    print(new_post, type(new_post),'--'*100)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print('JAKA JAKA',new_post)
    # cursor.execute("""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING * """,(post.title,post.content))
    # new_post = cursor.fetchone()
    # conn.commit()

    # post_dict = post.dict()
    # post_dict['id'] = randrange(1,100)
    # mposts.append(post_dict)
    # return {"posts":new_post} 
    return new_post


def find_post(id): 
    for post in mposts:
        if post['id'] == id:
            print(post)
            return post
    return None

@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()  
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()

    # if post is None:
    #     raise HTTPException(status_code=404, detail=f"Post not found for id {id}")
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"detail":f"post not found for id {id}"} 
    # print(post,'HELLPO')
    # return {"posts":id,"post":post}
    return post

@router.get("/latestpost")
def get_latest_post(): 
    lpost = mposts[-1]
    print(lpost)
    return {"posts":lpost}


def find_index(id):
    for p in mposts:
        if p['id'] == id:
            print(p,mposts.index(p))
            return mposts.index(p)

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db)): 
    
    post = db.query(models.Post).filter(models.Post.id == id)  
    
    if post.first() == None:
    # if deleted is None:
        raise HTTPException(status_code=404, detail=f"Post not found for id {id}")

    post.delete(synchronize_session=False)
    db.commit()
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """,(str(id),))
    # deleted = cursor.fetchone()
    # conn.commit() 

    
    # return {"posts":mposts,"detail":f"post {id} deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@router.put("/{id}",status_code=status.HTTP_200_OK) 
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db)):
    # print(updated_post,'JHAHAHAHAHAH')
    # cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s returning * """,(post.title,post.content,str(id))) 
    # updated = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post,'----'*200,id)
    if post == None:
        raise HTTPException(status_code=404, detail=f"Post not found for id {id}")
    try:
        post_query.update(updated_post.dict(),synchronize_session=False)
        print('REAC')
        db.commit()
    except Exception as e:
        raise e
    # mposts[index] = post.dict()
    # post_dict = post.dict()
    # post_dict['id'] = id
    # print(post_dict,'*'*30,post_dict['id'])
    # mposts[index] = post_dict
    # return {"posts":updated_post}
    return updated_post
