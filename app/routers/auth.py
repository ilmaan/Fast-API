from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from ..database import get_db

from .. import database

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_crediantials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email== user_crediantials.username).first()
    print("IN LOGIN URL")
    if not user:
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND, detail=f"invalid credentials")

    if not utils.verify(user_crediantials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND, detail=f"invalid credentials")
    print("FOUND USER",user)
    # TOKEN
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    # 

    print('access_token',access_token)
    return {"access_token":access_token,"token_type":"bearer"}