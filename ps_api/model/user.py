
from .db_model import DbModel


class User(DbModel):
    username: str
    email: str
    password_hash: str
    deleted: bool = False

