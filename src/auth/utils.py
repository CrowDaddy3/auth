import bcrypt


def hash_pasword(password: str) -> str:
    # Se convierte la contraseña a bytes
    password_bytes = password.encode('utf-8')
    # Se genera un salt y se hashea la contraseña
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Se convierte el hash en string para guardarlo
    return hashed_password.decode('utf-8')
