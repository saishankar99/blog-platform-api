def test_create_post_requires_auth(client):
    response = client.post("/posts/", json = {
        "title": "Hello", "content": "world"
    })

    assert response.status_code == 401

def test_create_post_success(client,auth_headers):
    response = client.post("/posts/", json={
        "title": "Hello", "content": "world"
    },headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Hello"
    assert data["author"]["email"] == "test@example.com"

def test_get_posts_is_public(client,auth_headers):
    client.post("/posts/", json = {
        "title": "Hello", "content": "world"
    },headers=auth_headers)

    response = client.get("/posts/")

    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_single_post_not_found(client):
    response = client.get('/posts/999')
    assert response.status_code == 404

def test_update_post_owner_success(client,auth_headers):
    create = client.post("/posts/", json = {
        "title": "Original", "content": "Gangster"
    },headers = auth_headers)
    post_id = create.json()["id"]
    response = client.patch(f"/posts/{post_id}", json = {
        "title": "dummy"
    },headers = auth_headers)

    assert response.status_code == 200
    assert response.json()["title"] == "dummy"

def test_update_post_wrong_owner(client,auth_headers):
    post = client.post("/posts/", json = {
        "title": "Uzumaki", "content": "Naruto"
    },headers = auth_headers)
    post_id = post.json()["id"]
    second_user = client.post("/users/register", json={
        "email": "alice@example.com", "password": "password123"
    })

    second_user_login = client.post("/users/login", data = {
        "username": "alice@example.com", "password": "password123"
    })

    intruder_headers = {"Authorization": f"Bearer {second_user_login.json()['access_token']}"}

    response = client.patch(f"/posts/{post_id}", json={
        "Title": "Monkey D"
    },headers = intruder_headers)

    assert response.status_code == 403

def test_delete_post_owner_success(client,auth_headers):
    create = client.post("/posts/", json= {
        "title": "deletable", "content": "post"
    }, headers = auth_headers)

    post_id = create.json()["id"]

    response = client.delete(f"/posts/{post_id}",headers = auth_headers)

    assert response.status_code == 204

    get_response = client.get(f"/posts/{post_id}")
    assert get_response.status_code == 404



