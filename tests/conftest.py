# tests/conftest.py
"""
Test configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base
from app.core.auth import create_user_account

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    try:
        user = create_user_account(
            db=db,
            username="testuser",
            email="test@example.com",
            password="testpass123",
            full_name="Test User"
        )
        yield user
    finally:
        db.close()

@pytest.fixture
def auth_headers(test_user):
    from app.core.auth import create_user_tokens
    tokens = create_user_tokens(test_user)
    return {"Authorization": f"Bearer {tokens['access_token']}"}