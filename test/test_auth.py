from fastapi.testclient import TestClient
from pymongo.database import Database

import ps_api.schema as s

from .data import TestData


def test_login(client: TestClient, db: Database, test_data: TestData):
    # login by username and password
    auth_data = s.UserLogin(
        username=test_data.test_users[0].username,
        password=test_data.test_users[0].password,
    )
    response = client.post(
        "api/auth/login",
        data=auth_data.model_dump(),
    )
    assert response and response.status_code == 200, "unexpected response"
    token = s.Token.model_validate(response.json())
    assert token and token.token_type == "Bearer"
    assert token.access_token

    # login by email and password
    auth_data = s.UserLogin(
        username=test_data.test_users[1].email,
        password=test_data.test_users[1].password,
    )
    response = client.post(
        "api/auth/login",
        data=auth_data.model_dump(),
    )
    assert response and response.status_code == 200, "unexpected response"
    token = s.Token.model_validate(response.json())
    assert token and token.token_type == "Bearer"
    assert token.access_token

    # login with invalid credentials
    auth_data = s.UserLogin(username="invalid", password="invalid")
    response = client.post(
        "api/auth/login",
        data=auth_data.model_dump(),
    )
    assert response and response.status_code == 403, "unexpected response"
    assert response.json() == {"detail": "Invalid credentials"}


def test_registration(client: TestClient, db: Database):
    TEST_USERNAME = "test"
    TEST_EMAIL = "some_email.simple2b@gamil.com"
    TEST_PASSWORD = "password1345"
    new_user = s.CreateUser(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD)
    response = client.post("api/auth/register", json=new_user.model_dump())
    assert response and response.status_code == 201

    user = s.User.model_validate(response.json())
    assert user and user.username == TEST_USERNAME
    assert user.email == TEST_EMAIL

    # check login
    auth_data = s.UserLogin(username=TEST_USERNAME, password=TEST_PASSWORD)
    response = client.post(
        "api/auth/login",
        data=auth_data.model_dump(),
    )
    assert response and response.status_code == 200, "unexpected response"
    token = s.Token.model_validate(response.json())
    assert token and token.token_type == "Bearer"
