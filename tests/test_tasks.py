from models.user import User

def create_user_and_token(client):
    client.post("/auth/register", json={
        "email": "task@test.com",
        "password": "123456"
    })

    response = client.post("/auth/login", json={
        "email": "task@test.com",
        "password": "123456"
    })

    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return headers


def test_create_task(client):
    headers = create_user_and_token(client)

    response = client.post("/tasks/", json={
        "title": "Test task",
        "description": "Test desc"
    }, headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Test task"
    assert data["completed"] is False


def test_get_task(client):
    headers = create_user_and_token(client)

    task = client.post("/tasks/", json={
        "title": "Task 1",
        "description": "Desc"
    }, headers=headers).json()

    response = client.get(f"/tasks/{task['id']}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == task["id"]


def test_get_task_not_found(client, db, auth_header):
    user = User(id=1, email="test@test.com")
    db.add(user)
    db.commit()

    response = client.get(
        "/tasks/999",
        headers=auth_header(user.id)
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(client):
    headers = create_user_and_token(client)

    task = client.post("/tasks/", json={
        "title": "Old",
        "description": "Old desc"
    }, headers=headers).json()

    response = client.put(f"/tasks/{task['id']}", json={
        "title": "New",
        "description": "New desc"
    }, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == "New"


def test_update_task_not_found(client, db, auth_header):
    user = User(id=1, email="test@test.com")
    db.add(user)
    db.commit()

    response = client.put(
        "/tasks/999",
        json={"title": "Nova", "description": "Teste"},
        headers=auth_header(user.id)
    )

    assert response.status_code == 404


def test_delete_task(client):
    headers = create_user_and_token(client)

    task = client.post("/tasks/", json={
        "title": "To delete",
        "description": "Desc"
    }, headers=headers).json()

    response = client.delete(f"/tasks/{task['id']}", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Deleted"


def test_delete_task_not_found(client, db, auth_header):
    user = User(id=1, email="test@test.com")
    db.add(user)
    db.commit()

    response = client.delete(
        "/tasks/999",
        headers=auth_header(user.id)
    )

    assert response.status_code == 404


def test_get_tasks_paginated(client):
    headers = create_user_and_token(client)

    for i in range(15):
        client.post("/tasks/", json={
            "title": f"Task {i}",
            "description": "Desc"
        }, headers=headers)

    response = client.get("/tasks/?page=1&page_size=10", headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 15
    assert len(data["items"]) == 10
    assert data["page"] == 1


def test_filter_completed(client):
    headers = create_user_and_token(client)

    task = client.post("/tasks/", json={
        "title": "Task",
        "description": "Desc"
    }, headers=headers).json()

    client.put(f"/tasks/{task['id']}", json={
        "title": "Task",
        "description": "Desc",
        "completed": True
    }, headers=headers)

    response = client.get("/tasks/?completed=true", headers=headers)

    assert response.status_code == 200
    assert response.json()["items"][0]["completed"] is True


def test_unauthorized_access(client):
    response = client.get("/tasks/")

    assert response.status_code in [401, 403]