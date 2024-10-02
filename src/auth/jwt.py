import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError
from config import settings


expires_in = settings.expire_time
secret_key = settings.secret_key
algorithm = settings.algorithm

def generate_jwt(data: dict) -> str:
    # Se calcula el tiempo en el que el token ya no sera valido
    expire = datetime.now(timezone.utc) +  timedelta(minutes=expires_in)
    payload = {**data, "exp": expire}
    # Se  genera un token con la información proporcionada
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def validate_token(token: str) -> str:
    try:
        print(token)
        # Se intenta desencriptar el token
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str =  payload.get("username")
        if not username:
            raise HTTPException(
                status_code=401,
                detail="Token vacio",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    # Manejo de excepciones especificas
    except ExpiredSignatureError:
        raise  HTTPException(
            status_code=401,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
