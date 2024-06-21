from fastapi import APIRouter, Depends

from ps_api import schema as s
from ps_api import controller as c
from ps_api import model as m

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/whoami", response_model=s.User)
def whoami(
    user: m.User = Depends(c.get_current_user),
):
    return user


@user_router.get("/greeting", response_model=s.Greeting)
def greeting(
    user: m.User = Depends(c.get_current_user),
):
    greeting_message = c.generate_greeting(user.username)
    return s.Greeting(message=greeting_message)
