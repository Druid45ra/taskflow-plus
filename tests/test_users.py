from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_registration():
    response = client.post("/users/register", json={
        "email": "test@example.com",
        "password": "secure123",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    assert "id" in response.json()
