from fastapi import FastAPI
from route import customer_routes
from connection import mongodb_connection

app = FastAPI(lifespan=mongodb_connection.lifespan)

""""
Pasos para completar el proyecto
-> crear todos los cruds sin base de datos (guardar en una lista)
    -> clientes 
    -> tarjetas
    -> cobros
-> Agregar base de datos a todos los cruds
-> Agregar inyección de dependencias a todo el proyecto
-> Agregar pruebas unitarias y que todas pasen
-> Agregar creación por defecto de colecciones y base de datos mongo
-> Dockerizar y pedir a Alan que verifique el proyecto
-> Revisar ajustes que pueda hacer para mejorarlo
"""
@app.get("/")
async def root():
    dbs = await app.mongodb_client.list_database_names()
    return {"databases": dbs}


app.include_router(customer_routes.router)
