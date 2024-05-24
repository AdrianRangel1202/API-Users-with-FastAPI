from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta, datetime

ALGORITHM = 'HS256'
access_token_duration = 1
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

router = APIRouter()
oath2 = OAuth2PasswordBearer(tokenUrl='/login')

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username : str
    full_name : str
    email : str
    disable : bool

class UserDB(User):
    password : str


users_bd = {
    "adrian":{
        "username" : "adrian",
        "full_name": "Adrian",
        "email" : "adrianrangel12@gmail.com",
        "disable" : False,
        "password": "$2a$12$D8iTa25NcJqaP3XHOiIQ7u3KIu1ETIXIAA0F8w9NQYwBK1T3mwiq2",
    },
    "Robert":{
        "username" : "Robert",
        "full_name": "Robert",
        "email" : "Robert12@gmail.com",
        "disable" : True,
        "password": "$2a$12$AxUU/Bg6Mhe.L57rsimyr.62bn.LIeO1M.YPsqIq7m03lVo3zV4g2",
    },
}


def search_user_db(username : str):
    if username in users_bd:
        return UserDB(**users_bd[username])
    
def search_user(username : str):
    if username in users_bd:
        return User(**users_bd[username])    
        
async def auth_user(token : str = Depends(oath2)):
    excepcion = HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="No Autorizado",
            headers={"WWW-Authenticate":"Bearer"})
        
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise excepcion
        

    except JWTError:
        raise excepcion

    return search_user(username)

    
async def current_user(user : User = Depends(auth_user)):
    
    if user.disable:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo",)
    
    return user


@router.post('/login')
async def login(form : OAuth2PasswordRequestForm = Depends()):
    users = users_bd.get(form.username)
    if not users:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail="Usuario No es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code= 404,detail="La contraseña es incorrecta")
    
    access_token_expiration = timedelta(minutes=access_token_duration) + datetime.utcnow()

    access_token = {
        "sub" : form.username,
        "exp" : access_token_expiration,

    }
    return{"access_token": jwt.encode(access_token,SECRET_KEY, algorithm=ALGORITHM), "token_type" : "bearer"}

@router.get('/users/me')
async def me(user : User = Depends(current_user)):
    return user
