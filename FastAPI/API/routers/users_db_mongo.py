from fastapi import APIRouter, HTTPException, status
#from pydantic import BaseModel
from db.models.user import User
from db.client import db_cliente
from db.Schemas.user import user_schemas, userEntity
from bson import ObjectId

router_user = APIRouter(prefix='/usersbd',
                        tags=['Usersdb'],
                        responses={status.HTTP_404_NOT_FOUND : {"mensaje":"No Found"}})

 


################ Funciones de uso interno ##########

def search_user(field : str, key):
    try:
        user = user_schemas(db_cliente.users.find_one({field: key}))
        return User(**user)
    
    except:
        return "NO SE HA ENCONTRADO EL USUARIO"


#                         ############# Metodos HTTP ###############

# /////////////////////// VISTA DE USUARIOS ////////////////////////////////////

# Mostrar todos los usuarios en DB 
@router_user.get('/', response_model= list[User])
async def Usersdb():
    return userEntity(db_cliente.users.find())

# Mostrar usuarios por Id 

@router_user.get('/{id}')
async def Usersdb(id : str):
    return search_user("_id", ObjectId(id))



# /////////////////////// CREACION DE USUARIOS ////////////////////////////////////

@router_user.post('/', status_code= status.HTTP_201_CREATED)
async def UserPost(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "USUARIO YA EXISTE")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_cliente.users.insert_one(user_dict).inserted_id

    new_user = user_schemas(db_cliente.users.find_one({"_id": id}))


    return User(**new_user)

# /////////////////////// ELIMINACION DE USUARIOS ////////////////////////////////////


@router_user.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def Del_user(id : str):

    found = db_cliente.users.find_one_and_delete({"_id" : ObjectId(id)})

    if not found :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= "EL USUARIO NO SE HA ELIMINADO")

# /////////////////////// ACTUALIZACION DE USUARIOS ////////////////////////////////////
    
@router_user.put('/', response_model= User)
async def Usersput(user: User):

    user_dict = dict(user)
    del user_dict["id"]
    try:
        
        db_cliente.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
        return search_user("_id", ObjectId(user.id))

    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= "EL USUARIO NO SE HA ACTUALIZADO")
