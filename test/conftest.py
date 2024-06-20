from typing import Generator
from dotenv import load_dotenv

load_dotenv("test/test.env")

# ruff: noqa: E402
import pytest
from pymongo.database import Database
from mongomock import MongoClient as MockMongoClient
from fastapi.testclient import TestClient
from ps_api import controller as c
from ps_api import model as m
from ps_api.database import get_db

from .data import TestData


@pytest.fixture
def test_data() -> Generator[TestData, None, None]:
    with open("test/data.json") as f:
        yield TestData.model_validate_json(f.read())


@pytest.fixture
def db(test_data: TestData) -> Generator[Database, None, None]:
    from ps_api import api

    db = MockMongoClient().db
    # Insert test data
    for u in test_data.test_users:
        # u.password_hash = c.make_hash(u.password)
        # db.users.insert_one(u.dict(exclude={"password": True}))
        db_user = m.User(username=u.username, email=u.email, password_hash=c.make_hash(u.password))
        db.users.insert_one(db_user.model_dump(exclude_none=True))

    def override_get_db() -> Generator[Database, None, None]:
        yield db

    api.dependency_overrides[get_db] = override_get_db

    yield db


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    from ps_api import api

    with TestClient(api) as c:
        yield c
