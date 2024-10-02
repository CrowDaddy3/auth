# tests/test_auth.py
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.db import Base, get_db

# Configurar una base de datos en memoria para pruebas
database_url = "sqlite:///./test.db"
engine = create_engine(database_url)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos de pruebas
Base.metadata.create_all(bind=engine)

# Dependencia de prueba
def override_get_db():
    try:
        db = TestingSession()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Código que se ejecuta antes de cada prueba
    Base.metadata.create_all(bind=engine)
    yield
    # Código que se ejecuta después de cada prueba
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def cleanup_db():
    yield
    # Código que se ejecuta después de que todos los tests hayan terminado
    if os.path.exists("test.db"):
        os.remove("test.db")

def test_register_user():
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "name": "Test", "last_name": "User ", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_register_existing_user():
    # Registrar un usuario
    client.post(
        "/auth/register",
        json={"username": "testuser", "name": "Test", "last_name": "User ", "password": "testpassword"},
    )
    # Intentar registrar el mismo usuario nuevamente
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "name": "Test", "last_name": "User ", "password": "testpassword"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username already exists"

def test_login_user():
    # Primero, registrar un usuario
    client.post(
        "/auth/register",
        json={"username": "testuser", "name": "Test", "last_name": "User ", "password": "testpassword"},
    )
    # Luego, intentar iniciar sesión
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "token" in data["data"]

def test_login_wrong_password():
    # Primero, registrar un usuario
    client.post(
        "/auth.register",
        json={"username": "testuser", "name": "Test", "last_name": "User ", "password": "testpassword"},
    )
    # Luego, intentar iniciar sesión con una contraseña incorrecta
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Wrong username or password"

def test_login_nonexistent_user():
    # Intentar iniciar sesión con un usuario que no existe
    response = client.post(
        "/auth/login",
        json={"username": "nonexistent", "password": "testpassword"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Wrong username or password"

def test_refresh_token():
    # Primero, registrar un usuario
    client.post(
        "/auth/register",
        json={"username": "testuser", "name": "Test", "last_name": "User ", "password": "testpassword"},
    )
    # Luego, iniciar sesión para obtener un token
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpassword"},
    )
    token = response.json()["data"]["token"]
    
    # Finalmente, refrescar el token
    response = client.post(
        "/auth/refresh-token",
        json={"token": token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "token" in data["data"]

def test_refresh_invalid_token():
    # Intentar refrescar un token inválido
    response = client.post(
        "/auth/refresh-token",
        json={"token": "invalidtoken"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid Token"

def test_validate_token():
    # Primero, registrar un usuario
    client.post(
        "/auth/register",
        json={"username": "testuser", "name": "Test", "last_name": "User ", "password": "testpassword"},
    )
    # Luego, iniciar sesión para obtener un token
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpassword"},
    )
    token = response.json()["data"]["token"]
    
    # Finalmente, validar el token
    response = client.post(
        "/auth/validate-token",
        json={"token": token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_validate_invalid_token():
    # Intentar validar un token inválido
    response = client.post(
        "/auth/validate-token",
        json={"token": "invalidtoken"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid Token"

def test_logout_user():
    response = client.post("/auth/logout")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Logged out successfully"