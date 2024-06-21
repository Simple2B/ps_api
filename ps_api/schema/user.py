from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str


class CreateUser(User):
    password: str


class Greeting(BaseModel):
    message: str

