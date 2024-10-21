from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

# Utility function to get JWT token
def get_auth_token():
    response = client.post("/token", data={"username": "user1", "password": "password123"})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_create_product():
    token = get_auth_token()
    response = client.post("/products", json={"title": "Test product", "description": "A test product", "price": 10.0},
                           headers={"Authorization": f"Bearer {token}"},)
    assert response.status_code == 201
    assert response.json()["title"] == "Test product"

def test_get_products():
    token = get_auth_token()
    response = client.get("/products",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)