from jose import jwt
from models.user import User
from core.config import SECRET_KEY, ALGORITHM
from api.deps import get_db


def test_get_db_closes():
    gen = get_db()

    db = next(gen)
    assert db is not None

    try:
        next(gen)
    except StopIteration:
        pass


def test_get_current_user_success(client, db):
    user = User(id=1, email="test@test.com")
    db.add(user)
    db.commit()

    token = jwt.encode({"sub": "1"}, SECRET_KEY, algorithm=ALGORITHM)

    response = client.get(
        "tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_get_current_user_invalid_token(client):
    response = client.get(
        "tasks/",
        headers={"Authorization": "Bearer token_invalido"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_get_current_user_no_sub(client):
    token = jwt.encode({}, SECRET_KEY, algorithm=ALGORITHM)

    response = client.get(
        "tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_get_current_user_not_found(client):
    token = jwt.encode({"sub": "999"}, SECRET_KEY, algorithm=ALGORITHM)

    response = client.get(
        "tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "User not found"