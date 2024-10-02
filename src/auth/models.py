from sqlalchemy import Column, Integer, String
from db import Base


class User(Base):
    __tablename__ = "user"

    id: int =  Column(Integer, primary_key=True, index=True)
    username: str = Column(String, index=True, unique=True)
    name: str = Column(String, index=True)
    last_name: str = Column(String)
    password : str = Column(String)
