from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..backend.database import Base
from ..backend.main import app, get_db
from ..backend import schemas

# Configurar base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Usa SQLite para pruebas
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base de datos y tablas para pruebas
Base.metadata.create_all(bind=engine)

# Dependency override para usar la base de datos de prueba
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Pruebas para User
def test_create_user():
    response = client.post("/users/", json={"username": "testuser", "email": "testuser@example.com", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"

def test_get_user():
    response = client.post("/users/", json={"username": "testuser2", "email": "testuser2@example.com", "password": "password123"})
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser2"
    assert data["email"] == "testuser2@example.com"

# Pruebas para Category
def test_create_category():
    response = client.post("/categories/", json={"name": "TestCategory"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestCategory"

def test_get_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0  # Asegurarse de que haya al menos una categoría

# Pruebas para Project
def test_create_project():
    # Crear un usuario primero
    user_response = client.post("/users/", json={"username": "projectuser", "email": "projectuser@example.com", "password": "password123"})
    user_id = user_response.json()["id"]
    # Crear una categoría
    category_response = client.post("/categories/", json={"name": "ProjectCategory"})
    category_id = category_response.json()["id"]

    # Crear el proyecto
    response = client.post("/projects/", json={
        "name": "Test Project",
        "description": "A project for testing",
        "category_id": category_id,
        "user_id": user_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "A project for testing"

def test_get_project():
    # Crear un proyecto para obtenerlo
    user_response = client.post("/users/", json={"username": "getprojectuser", "email": "getprojectuser@example.com", "password": "password123"})
    user_id = user_response.json()["id"]
    category_response = client.post("/categories/", json={"name": "GetProjectCategory"})
    category_id = category_response.json()["id"]
    project_response = client.post("/projects/", json={
        "name": "Another Test Project",
        "description": "Another project for testing",
        "category_id": category_id,
        "user_id": user_id
    })
    project_id = project_response.json()["id"]

    # Obtener el proyecto
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Another Test Project"
    assert data["description"] == "Another project for testing"
