from datetime import datetime
from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str
    exp: datetime | None = None
