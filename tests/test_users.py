from fastapi import status
from jose import jwt
from app import schemas
import pytest

from app.config import settings


def test_create_user(client):
    response = client.post(
        "/users/", json={"email": "testuser12@gmail.com", "password": "12345"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "testuser12@gmail.com"
    assert response.status_code == status.HTTP_201_CREATED


def test_login_user(test_user, client):
    response = client.post(
        "/login", data={"username": test_user['email'],
                        "password": test_user['password']})
    login_res = schemas.Token(**response.json())
    assert login_res.access_token is not None
    payload = jwt.decode(login_res.access_token,
                         settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("email, password, status_code",
                         [("wrongemail@gmail.com", "12345", status.HTTP_403_FORBIDDEN),
                          ("testuser@gmail.com", "wrongpassword",
                           status.HTTP_403_FORBIDDEN),
                          ("wrongemail@gmail.com", "wrongpassword",
                           status.HTTP_403_FORBIDDEN),
                          (None, "12345", status.HTTP_422_UNPROCESSABLE_ENTITY),
                          ("testuser@gmail.com", None,
                           status.HTTP_422_UNPROCESSABLE_ENTITY),
                          ])
def test_incorrect_login(client, email, password, status_code):
    response = client.post(
        "/login", data={"username": email, "password": password})

    assert response.status_code == status_code
