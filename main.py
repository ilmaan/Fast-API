from fastapi import FastAPI
from models import User, Gender, Role
from typing import List
from uuid import UUID,uuid4

app = FastAPI()

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
