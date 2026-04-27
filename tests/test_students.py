import pytest
from app import app, db, generate_token

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def get_jwt_header(user_id=1, role="admin"):
    token = generate_token(user_id, role)
    return {"Authorization": f"Bearer {token}"}

def test_add_student_api(client):
    response = client.post("/student",
        json={"name": "Milan", "age": 23, "major": "Math"},
        headers=get_jwt_header())
    assert response.status_code == 201
    assert b"Student added successfully" in response.data

def test_get_students_api(client):
    response = client.get("/students", headers=get_jwt_header())
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_student_api(client):
    # Dodaj studenta
    client.post("/student",
        json={"name": "Petar", "age": 20, "major": "Physics"},
        headers=get_jwt_header())

    # Update studenta sa ID=1 (primer)
    response = client.put("/student/1",
        json={"name": "Petar", "age": 21, "major": "Physics"},
        headers=get_jwt_header())
    assert response.status_code == 200
    assert b"Student updated successfully" in response.data

def test_delete_student_api(client):
    response = client.delete("/student/1", headers=get_jwt_header())
    assert response.status_code == 200
    assert b"Student deleted successfully" in response.data
