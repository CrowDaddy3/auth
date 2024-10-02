from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from .models import User
from .schemas import CreateUser, UserRead
from .utils import hash_pasword


router = APIRouter(prefix="/auth")


@router.post("/register", tags=["registro"], response_model=UserRead)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    user_ = db.query(User).filter(User.username == user.username).first()
    if user_:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_ = User(
        username=user.username,
        name=user.name,
        last_name=user.last_name,
        password=hash_pasword(user.password)
        )
    
    db.add(user_)
    db.commit()
    db.refresh(user_)
    return user_
