from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from ..backend.database import Base
from ..backend.main import app, get_db
from ..backend import schemas

# Configurar base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Usa SQLite para pruebas
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base de datos y tablas para pruebas
Base.metadata.create_all(bind=engine)

# Instancia de Faker
fake = Faker()

# Dependency override para usar la base de datos de prueba
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Pruebas para User con Faker
def test_create_user():
    username = fake.user_name()
    email = fake.email()
    response = client.post("/users/", json={"username": username, "email": email, "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert data["email"] == email

def test_get_user():
    username = fake.user_name()
    email = fake.email()
    response = client.post("/users/", json={"username": username, "email": email, "password": "password123"})
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert data["email"] == email

# Pruebas para Category con Faker
def test_create_category():
    category_name = fake.word()
    response = client.post("/categories/", json={"name": category_name})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == category_name

def test_get_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0  # Asegurarse de que haya al menos una categoría

# Pruebas para Project con Faker
def test_create_project():
    # Crear un usuario primero
    user_response = client.post("/users/", json={"username": fake.user_name(), "email": fake.email(), "password": "password123"})
    user_id = user_response.json()["id"]
    
    # Crear una categoría
    category_response = client.post("/categories/", json={"name": fake.word()})
    category_id = category_response.json()["id"]

    # Crear el proyecto
    project_name = fake.sentence(nb_words=3)
    project_description = fake.text(max_nb_chars=50)
    response = client.post("/projects/", json={
        "name": project_name,
        "description": project_description,
        "category_id": category_id,
        "user_id": user_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == project_name
    assert data["description"] == project_description

def test_get_project():
    # Crear un proyecto para obtenerlo
    user_response = client.post("/users/", json={"username": fake.user_name(), "email": fake.email(), "password": "password123"})
    user_id = user_response.json()["id"]
    category_response = client.post("/categories/", json={"name": fake.word()})
    category_id = category_response.json()["id"]
    project_name = fake.sentence(nb_words=3)
    project_description = fake.text(max_nb_chars=50)
    project_response = client.post("/projects/", json={
        "name": project_name,
        "description": project_description,
        "category_id": category_id,
        "user_id": user_id
    })
    project_id = project_response.json()["id"]

    # Obtener el proyecto
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == project_name
    assert data["description"] == project_description
