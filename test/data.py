from pydantic import BaseModel
from ps_api import schema as s


class TestData(BaseModel):
    __test__ = False

    test_users: list[s.CreateUser]
