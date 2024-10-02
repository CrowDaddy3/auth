from fastapi import FastAPI
from db import Base, engine

# Se crean las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Creamos la aplicación 
app = FastAPI()

#Ruta raiz
@app.get("/")
def root():
    return {"message": "Pagina de inicio"}