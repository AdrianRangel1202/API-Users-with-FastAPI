from fastapi import APIRouter

router_prod = APIRouter(prefix='/products', 
                        responses={404 : {"mensaje":"no encontrado"}},
                        tags=['Products'])


list_products = ['product 1','product 2','product 3','product 4',]

@router_prod.get('/')
async def products():   
    return list_products

@router_prod.get('/{id:int}')
async def products(id : int):   
    return list_products[id]