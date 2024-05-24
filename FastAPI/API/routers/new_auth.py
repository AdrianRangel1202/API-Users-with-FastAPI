from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
auth = OAuth2PasswordBearer(tokenUrl='/token')



users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password": "123456"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password": "654321"
    }
}

#Lo que retorne la funcion de POST es lo que sera como parametro de la funcion GET
#En este caso "token" tiene almacenado lo que devolvio la funcion POST
@app.get('/users/me')
async def users_get(token : str  = Depends(auth)):
    user = users_db.get(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Usuario No Autorizado',
                            headers= {"WWW-Authenticate":"Bearer"})
    return 'Has ingresado en esta ruta'

@app.post('/token')
async def users_post(form : OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='Usuario No Encontrado')
    if not form.password == user['password']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Contraseña Incorrecta')
    return {
        'access_token': form.username,
        'token_type': 'bearer'
        }