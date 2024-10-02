from fastapi import FastAPI
from db import Base, engine
from auth import router

# Se crean las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Creamos la aplicación 
app = FastAPI()

app.include_router(router.router)


#Ruta raiz
@app.get("/")
def root():
    return {"message": "Pagina de inicio"}
