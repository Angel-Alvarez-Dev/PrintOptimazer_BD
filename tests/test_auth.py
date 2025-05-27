# tests/test_auth.py
"""
Authentication tests
"""
import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    """Test user registration"""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpass123",
        "full_name": "New User"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_login_user(client: TestClient, test_user):
    """Test user login"""
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    login_data = {
        "username": "wronguser",
        "password": "wrongpass"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401
