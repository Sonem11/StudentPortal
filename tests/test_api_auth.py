import pytest
import uuid
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def get_token(client, username, password):
    # Registracija korisnika
    client.post("/register", data={
        "username": username,
        "password": password
    }, follow_redirects=True)

    # Login preko API-ja
    response = client.post("/api/login", json={
        "username": username,
        "password": password
    })
    return response.get_json()["token"]

def test_api_login_and_get_students(client):
    username = f"api_{uuid.uuid4().hex[:6]}"
    password = "api_pass"
    token = get_token(client, username, password)

    response = client.get("/students", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_api_add_update_delete_student(client):
    username = f"api_crud_{uuid.uuid4().hex[:6]}"
    password = "api_pass"
    token = get_token(client, username, password)

    # Dodaj studenta
    response = client.post("/student", json={
        "name": "Test Student",
        "age": 21,
        "major": "Math"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.get_json()["message"] == "Student added successfully"

    # Preuzmi listu studenata da dobijemo ID
    students = client.get("/students", headers={
        "Authorization": f"Bearer {token}"
    }).get_json()
    student_id = students[0][0]  # pretpostavka: prvi student, kolona 0 = id

    # Update studenta
    response = client.put(f"/student/{student_id}", json={
        "name": "Updated Student",
        "age": 22,
        "major": "Physics"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Student updated successfully"

    # Delete studenta
    response = client.delete(f"/student/{student_id}", headers={
        "Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Student deleted successfully"
