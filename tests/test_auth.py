def test_register(client):
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "123456"
    })

    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "test@test.com"
    assert "id" in data


def test_login(client):
    client.post("auth/register", json={
        "email": "login@test.com",
        "password": "123456"
    })

    response = client.post("auth/login", json={
        "email": "login@test.com",
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid(client):
    response = client.post("auth/login", json={
        "email": "wrong@test.com",
        "password": "wrong"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"


def test_token(client):
    client.post("auth/register", json={
        "email": "oauth@test.com",
        "password": "123456"
    })

    response = client.post("auth/token", data={
        "username": "oauth@test.com",
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token(client):
    client.post("auth/register", json={
        "email": "refresh@test.com",
        "password": "123456"
    })

    login = client.post("auth/login", json={
        "email": "refresh@test.com",
        "password": "123456"
    })

    token = login.json()["access_token"]

    response = client.get("auth/refresh", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_token_user_not_found(client):
    response = client.post("/auth/token", data={
        "username": "naoexiste@test.com",
        "password": "123456"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"


def test_token_wrong_password(client):
    client.post("/auth/register", json={
        "email": "user@test.com",
        "password": "123456"
    })

    response = client.post("/auth/token", data={
        "username": "user@test.com",
        "password": "senha_errada"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"
