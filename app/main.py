from cgi import test
from pyexpat import model
from fastapi import FastAPI, Response,status, HTTPException, Depends 
from models import User, Gender, Role
from typing import List, Optional
from uuid import UUID,uuid4
from pydantic import BaseModel 
from random import randrange     
from fastapi.params import Body
import psycopg2 
from sqlalchemy.orm import Session 
from psycopg2.extras import RealDictCursor
import time
from . import  models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

# Creating Object for FastAPI
app = FastAPI()



class Post(BaseModel): 
    title: str
    content: str

# RAW CONNECTION TO DATABASE
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fast-api',user='postgres',password='1234',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to the database")
        break
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error) 
        time.sleep(2)



@app.post("/createpost")
def create_post(post:Post):
    print(post, type(post)) 
    p = post.dict()
    print(type(p))

    return {"title":post.title,"content":post.content,"p":p}  

# SQL ALCHEMY  CONNECTION
@app.get("/sqlalchemy")
def get_sqlalchemy(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post 


mposts = [{"id":1,"title":"title1","content":"content1"},{"id":2,"title":"title2","content":"content2"}]

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"posts":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post, db: Session = Depends(get_db)):
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
    return {"posts":new_post} 


def find_post(id): 
    for post in mposts:
        if post['id'] == id:
            print(post)
            return post
    return None

@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()  
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()

    # if post is None:
    #     raise HTTPException(status_code=404, detail=f"Post not found for id {id}")
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"detail":f"post not found for id {id}"} 
    # print(post,'HELLPO')
    return {"posts":id,"post":post}

@app.get("/latestpost")
def get_latest_post(): 
    lpost = mposts[-1]
    print(lpost)
    return {"posts":lpost}


def find_index(id):
    for p in mposts:
        if p['id'] == id:
            print(p,mposts.index(p))
            return mposts.index(p)

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db)): 
    
    post = db.query(models.Post).filter(models.Post.id == id).first()  
    
    if post.first() == None:
    # if deleted is None:
        raise HTTPException(status_code=404, detail=f"Post not found for id {id}")


    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """,(str(id),))
    # deleted = cursor.fetchone()
    # conn.commit() 

    
    # return {"posts":mposts,"detail":f"post {id} deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put("/posts/{id}",status_code=status.HTTP_200_OK) 
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s returning * """,(post.title,post.content,str(id))) 
    updated = cursor.fetchone()
    conn.commit()
    if updated == None:
        raise HTTPException(status_code=404, detail=f"Post not found for id {id}")
    # mposts[index] = post.dict()
    # post_dict = post.dict()
    # post_dict['id'] = id
    # print(post_dict,'*'*30,post_dict['id'])
    # mposts[index] = post_dict
    return {"posts":updated}






db: List[User] = [
        User(id=uuid4(),fname='ilmaan',lname='zia',gender=Gender.male,roles=[Role.admin]),
        User(id=uuid4(),fname='sahiba',lname='kaur',gender=Gender.female,roles=[Role.user])
        ]

        
@app.get("/")
async def root():
    return {"message": "BALe Hello World"}


@app.get("/men")
async def root():
    return {"ma": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int): 
    return {"item_id": item_id}

@app.get("/api/v1/user")
async def fetch():
    return db;

@app.post("/api/v1/user")
async def regis(user:User):
    db.append(user)
    return {"id":user.id}
