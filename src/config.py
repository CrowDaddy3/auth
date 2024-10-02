import os
from pydantic_settings import BaseSettings
from pydantic import ValidationError
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    # Se declaran las variables de entorno a utilizar
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm : str = os.getenv("ALGORITHM", "HS256")
    expire_time: int = os.getenv("EXPIRE_TIME", 10)
    database_url: str = os.getenv("DATABASE_URL")

# Se crea una instancia de settings para consumo de variables de entorno
try:
    settings = Settings()
except ValidationError as e:
    print(e, "*"*100)