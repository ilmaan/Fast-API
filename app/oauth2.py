import imp
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET KEY
# ALGORITHM
# EXPIRATION TIME

SECRET_KEY = "123456789qwertyu987654321"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms= ALGORITHM)

        id: str = payload.get("user_id")

        if id in None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)   
    except  :
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could Not valiatet", headers={"WWW=Authenticate":"Bearer"})
    
    return verify_access_token(token, credentials_exception)