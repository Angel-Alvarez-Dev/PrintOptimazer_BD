# tests/test_materials.py
"""
Material API tests
"""
import pytest
from fastapi.testclient import TestClient

def test_create_material(client: TestClient, auth_headers):
    """Test material creation"""
    material_data = {
        "name": "Test PLA",
        "material_type": "filament",
        "cost_per_unit": 25.0,
        "current_stock": 3.0,
        "unit": "kg"
    }
    
    response = client.post(
        "/api/v1/materials/", 
        json=material_data, 
        headers=auth_headers
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == material_data["name"]
    assert data["cost_per_unit"] == material_data["cost_per_unit"]

def test_get_materials(client: TestClient, auth_headers):
    """Test getting materials"""
    response = client.get("/api/v1/materials/", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)