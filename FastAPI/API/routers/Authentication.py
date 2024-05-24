from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



#Autenticacion basica (usuario y contraseña)

auth = FastAPI()
oath2 = OAuth2PasswordBearer(tokenUrl='/login')

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
        "password": "123456",
    },
    "Robert":{
        "username" : "Robert",
        "full_name": "Robert",
        "email" : "Robert12@gmail.com",
        "disable" : True,
        "password": "654321",
    },
}


def search_user_db(username : str):
    if username in users_bd:
        return UserDB(**users_bd[username])
    

def search_user(username : str):
    if username in users_bd:
        return User(**users_bd[username])    

async def current_user(token : str = Depends(oath2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="No Autorizado",
            headers={"WWW-Authenticate":"Bearer"})
    
    if user.disable:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo",)
    
    return user


@auth.post('/login')
async def login(form : OAuth2PasswordRequestForm = Depends()):
    users = users_bd.get(form.username)
    if not users:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail="Usuario No es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code= 404,detail="La contraseña es incorrecta")
    
    return{"access_token": user.username, "token_type" : "bearer"}

@auth.get('/users/me')
async def me(user : User = Depends(current_user)):
    return user
