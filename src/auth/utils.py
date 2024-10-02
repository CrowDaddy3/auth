import bcrypt


def hash_pasword(password: str) -> str:
    # Se convierte la contraseña a bytes
    password_bytes = password.encode('utf-8')
    # Se genera un salt y se hashea la contraseña
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Se convierte el hash en string para guardarlo
    return hashed_password.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    # Se convierte la contraseña a bytes
    password_bytes =  password.encode('utf-8')
    # Se convierte la contraseña hasehada a bytes
    hashed_password_bytes = hashed_password.encode('utf-8')
    #  Se compara la contraseña con el hash
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)