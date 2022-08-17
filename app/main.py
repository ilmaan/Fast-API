from fastapi import FastAPI, Response,status, HTTPException
from models import User, Gender, Role
from typing import List, Optional
from uuid import UUID,uuid4
from pydantic import BaseModel 
from random import randrange     
from fastapi.params import Body
import psycopg2 
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel): 
    title: str
    content: str

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


mposts = [{"id":1,"title":"title1","content":"content1"},{"id":2,"title":"title2","content":"content2"}]

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"posts":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING * """,(post.title,post.content))
    new_post = cursor.fetchone()
    conn.commit()

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
def get_post(id: int, response: Response):   
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post not found for id {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail":f"post not found for id {id}"} 
    print(post)
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
def delete_post(id: int, response: Response):
    index = find_index(id)
    print(index)
    if not index:
        raise HTTPException(status_code=404, detail=f"Post not found for id {id}")
    mposts.pop(index)
    # return {"posts":mposts,"detail":f"post {id} deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put("/posts/{id}",status_code=status.HTTP_200_OK) 
def update_post(id: int, post: Post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=404, detail=f"Post not found for id {id}")
    # mposts[index] = post.dict()
    post_dict = post.dict()
    post_dict['id'] = id
    print(post_dict,'*'*30,post_dict['id'])
    mposts[index] = post_dict
    return {"posts":post_dict}






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
