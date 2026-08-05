def test_register_success(client):
    response = client.post("/users/register",json={
        "email":"alice@example.com", "password": "password124"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "alice@example.com"
    assert "password" not in response.json()
    assert "hashed_password" not in response.json()

def test_register_duplicate_email(client):
    client.post("/users/register", json={
        "email": "alice@example.com" , "password": "password123"
    })
    response = client.post("/users/register", json={
        "email": "alice@example.com", "password": "password123"
    })

    assert response.status_code == 409

def test_login_success(client):
    client.post("/users/register", json = {
        "email": "alice@example.com", "password": "password123"
    })
    response = client.post("/users/login", data={
        "username": "alice@example.com", "password": "password123"
    })
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()

def test_login_with_wrong_password(client):
    client.post("/users/register", json={
        "email": "alice@example.com", "password": "password123"
    })
    response = client.post("/users/login", data={
        "username": "alice@example.com", "password": "password143"
    })

    assert response.status_code == 401

def test_me_without_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401

def test_me_with_token(client,auth_headers):
    response = client.get("/users/me",headers = auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
