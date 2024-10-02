from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse 
from sqlalchemy.orm import Session
from db import get_db
from .models import User
from .schemas import CreateUser, UserRead, Auth, Token
from .utils import hash_pasword, check_password
from .jwt import generate_jwt, validate_token as vt


router = APIRouter(prefix="/auth")


@router.post("/register", tags=["Registro"], response_model=UserRead)
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
    
    # Se crea el usuario en la base de datos
    db.add(user_)
    db.commit()
    db.refresh(user_)
    return user_

@router.post("/login", tags=["Autenticación"])
def login(user: Auth, db: Session = Depends(get_db)):
    # Verificar si el usuario existe
    user_ = db.query(User).filter(User.username == user.username).first()
    if not user_:
        raise HTTPException(
            status_code=401,
            detail="Wrong username or password",
        )
    
    if not check_password(user.password, user_.password):
        raise HTTPException(
            status_code=401,
            detail="Wrong username or password",
        )
    
    #Se genera el token
    token = generate_jwt(
        data={"username": user_.username}
    )

    response: dict = {"token": token, "token_type": "bearer"}

    return JSONResponse(content={"data": response})

@router.post("/refresh-token", tags=["Autenticación"])
def refresh_token(token: Token, db: Session = Depends(get_db)):
    # Verificar si el token es válido
    user: str = vt(token.token)
    if user:
        user_ = db.query(User).filter(User.username == user).first()
        if not user_:
            raise HTTPException(
                status_code=400,
                detail="Invalid Token",
                headers={"WWW-Autenticate": "Bearer"}
            )
        # Se genera un nuevo token
        token =  generate_jwt(data={"username": user_.username})
        response: dict = {"token": token, "token_type": "bearer"}
        return JSONResponse(content={"data": response})
    
@router.post(
    "/validate-token", tags=["Autenticación"], response_model=UserRead)
def validate_token(token: Token, db: Session = Depends(get_db)):
    # Verificar si el token es válido
    user: str = vt(token.token)
    if user:
        #  Se obtiene el usuario
        user_ = db.query(User).filter(User.username == user).first()
        if not user_:
            raise HTTPException(
                status_code=400,
                detail="Invalid Token",
                headers={"WWW-Autenticate": "Bearer"}
            )
        return user_

@router.post("/logout", tags=["Autenticación"])
def logout():
    # Cierra sesión
    return JSONResponse(content={"message": "Logged out successfully"})