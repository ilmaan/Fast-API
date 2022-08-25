from .. import models, schemas, utils
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from ..database import get_db
 
router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def  create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):

    # HASHING THE PASSWORD
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    print(new_user, type(new_user),'--'*100)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 

    return new_user 


@router.get("/{id}",response_model=schemas.UserOut )
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"No User found for id {id}")

    return user

@router.get("/" )
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    if not user:
        raise HTTPException(status_code=404, detail=f"No User founds")

    return user








