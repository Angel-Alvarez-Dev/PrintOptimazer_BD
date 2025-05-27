# tests/test_projects.py
"""
Project API tests
"""
import pytest
from fastapi.testclient import TestClient

def test_create_project(client: TestClient, auth_headers):
    """Test project creation"""
    project_data = {
        "name": "Test Project",
        "description": "A test project",
        "client_name": "Test Client",
        "platform": "direct",
        "budget": 500.0
    }
    
    response = client.post(
        "/api/v1/projects/", 
        json=project_data, 
        headers=auth_headers
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["budget"] == project_data["budget"]

def test_get_projects(client: TestClient, auth_headers):
    """Test getting projects"""
    response = client.get("/api/v1/projects/", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_unauthorized_access(client: TestClient):
    """Test unauthorized access to projects"""
    response = client.get("/api/v1/projects/")
    assert response.status_code == 401