from fastapi import FastAPI
from routers import products, users, auth_jwt, users_db_mongo
from fastapi.staticfiles import StaticFiles
app = FastAPI()

#Router Products y users
app.include_router(products.router_prod)
app.include_router(users.router_user)
app.include_router(auth_jwt.router)
app.include_router(users_db_mongo.router_user)

#app.mount('/statics', StaticFiles(directory='static'), name='static')


@app.get('/')
async def root():
    return 'Hola Mundo'

@app.get('/mensaje')
async def root2():
    return {'mensaje': 2}
