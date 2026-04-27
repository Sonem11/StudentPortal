import pytest
from app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_register_and_login(client):
    # Registracija novog korisnika
    response = client.post("/register", data={
        "username": "testuser",
        "password": "testpass"
    }, follow_redirects=True)
    assert response.status_code == 200

    # Login sa tim korisnikom
    response = client.post("/login", data={
        "username": "testuser",
        "password": "testpass"
    }, follow_redirects=True)
    assert b"Logged in as: testuser" in response.data

def test_logout(client):
    # Login prvo
    client.post("/login", data={
        "username": "testuser",
        "password": "testpass"
    }, follow_redirects=True)

    # Logout
    response = client.get("/logout", follow_redirects=True)
    assert b"Login" in response.data
