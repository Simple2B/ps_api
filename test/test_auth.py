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
        auth_data.model_dump(),
    )
    assert response and response.status_code == 200, "unexpected response"


def test_signup(client: TestClient, db: Database, test_data: TestData):
    response = client.post("api/auth/sign-up", json=test_data.test_user.dict())
    assert response and response.status_code == 201
    assert db.users.find_one({"email": test_data.test_user.email})
