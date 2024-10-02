from sqlalchemy import Colum, Integer, String
from db import Base


class User(Base):
    __tablename__ = "users"

    id: int =  Colum(Integer, primary_key=True, index=True)
    username: str = Colum(String, index=True, unique=True)
    name: str = Colum(String, index=True)
    last_name: str = Colum(String)
    password : str = Colum(String)