from fastapi.testclient import TestClient
from pymongo.database import Database

import ps_api.schema as s

from .data import TestData


def test_whoami(client: TestClient, db: Database, test_data: TestData):
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

    client.headers["Authorization"] = f"Bearer {token.access_token}"

    response = client.get("api/user/whoami")
    assert response and response.status_code == 200, "unexpected response"
    me = s.User.model_validate(response.json())
    assert me and me.username == test_data.test_users[0].username
    assert me.email == test_data.test_users[0].email
