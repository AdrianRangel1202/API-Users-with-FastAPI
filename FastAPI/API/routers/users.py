from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router_user = APIRouter(prefix='/users',
                        tags=['Users'],
                        responses={404 : {"mensaje":"No Found"}})

 
############### HTTP GET ################

# MOdelar una clase para crear objetos de usuarios

class User(BaseModel):
    id: int
    name : str
    surname : str
    age : int

users_list = [  User(id= 1, name= 'rober', surname= 'Carlos', age= 20),
                User(id= 2,name= 'Pedro', surname= 'Juan', age= 24),
                User(id= 3,name= 'Martinez', surname= 'Marcos', age= 26),]

@router_user.get('/usersclass')
async def Usersclass():
    return users_list



@router_user.get('/user/{id}')
async def Users(id : int):
    usuario = filter(lambda user: user.id == id, users_list)
    try:
        return list(usuario)[0] 
    except:
        return 'No se ha encontrado el usuario'
    
@router_user.get('/Usersquery')
async def Users_in_list(skip:int = 0, limit:int = 3):
    return users_list[skip : skip + limit]

# http://127.0.0.1:8000/Usersquery/?skip=1&limit=3
# Esta es la manera de pasar los parametros de la funcion query
# Usando el signo de interrogacion "?" y dandelos los valores
# Separados por el signo "&"




############### HTTP POST ################

@router_user.post('/new_user/', status_code= 201)
async def UserPost(user: User):
    if type(Valid_user(user.id)) == User:
        raise HTTPException(status_code= 404,detail="Usuario Ya Existe")
    else:
        users_list.append(user)

def Valid_user(id : int):
    usuario = filter(lambda user: user.id == id, users_list)
    try:
        return list(usuario)[0] 
    except:
        return 'No se ha encontrado el usuario'



############### HTTP PUT ################
    
@router_user.put('/actualize_user')
async def Usersput(user: User):

    Verific = False

    for index, Us in enumerate(users_list):
        if Us.id == user.id:
            users_list[index] = user
            Verific = True
        
    if not Verific:
        return 'No se ha Podido Actualizar el usuario'
    return user


############### HTTP DELETE ################

@router_user.delete('/delete_user/{id}')
async def Del_user(id : int):

    for user in users_list:
        if user.id == id:
            users_list.remove(user)
            return 'El usuario a sido eliminado con Exito'
            
        else: 
            return 'Ha ocurrido un error'