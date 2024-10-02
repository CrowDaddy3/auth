from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

#Se declara el path de la base de datos
database_url = settings.database_url

#Se inicia el  motor de la base de datos
engine = create_engine(database_url)

#Se crea la sesion
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Se crea la base de datos
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
