from pymongo import MongoClient


# Usaremos el .local para indicar que estaremos conectado en estado local
# Esto puede no colocarse solo que sera colocado cada vez que se llame la instancia 
db_cliente = MongoClient().local