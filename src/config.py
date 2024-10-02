from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Se declaran las variables de entorno a utilizar
    database_url: str

    class Config:
        env_file = ".env"


# Se crea una instancia de settings para consumo de variables de entorno
settings = Settings()