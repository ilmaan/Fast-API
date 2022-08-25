from cgi import test
import imp
# from msilib import schema
# from multiprocessing import synchronize
from pyexpat import model
# from turtle import pos
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
from . import  models, schemas, utils
from .database import engine, get_db

from .routers import user,post,auth


models.Base.metadata.create_all(bind=engine)

# Creating Object for FastAPI
app = FastAPI()



app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router) 



# MOVED TO SCHEMAS FILE
# class Post(BaseModel): 
#     title: str
#     content: str

# RAW CONNECTION TO DATABASE
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fast_test',user='postgres',password='1234',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected to the database")
#         break
#     except (Exception, psycopg2.Error) as error :
#         print ("Error while connecting to PostgreSQL", error) 
#         time.sleep(2)



@app.post("/createpost")
def create_post(post:schemas.PostCreate):
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

