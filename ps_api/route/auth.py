from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pymongo.database import Database
from pymongo import results

from ps_api.database import get_db
from ps_api.logger import log
from ps_api import schema as s
from ps_api import controller as c
from ps_api import model as m


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login", response_model=s.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Database = Depends(get_db),
):
    res = db.users.find_one(
        {
            "$or": [
                {"username": user_credentials.username},
                {"email": user_credentials.username},
            ]
        }
    )
    user = m.User.model_validate(res) if res else None
    if not user or not c.hash_verify(user_credentials.password, user.password_hash):
        log(log.ERROR, "User [%s] was not authenticated", user_credentials.username)
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = c.create_access_token(s.TokenData(user_id=str(user.id)))

    return s.Token(access_token=access_token, token_type="Bearer")


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=s.User,
)
def register(
    data: s.CreateUser,
    db: Database = Depends(get_db),
):
    new_user = m.User(
        username=data.username,
        email=data.email,
        password_hash=c.make_hash(data.password),
    )
    res: results.InsertOneResult = db.users.insert_one(new_user.model_dump())

    log(log.INFO, "User [%s] registered", data.email)
    return db.users.find_one({"_id": res.inserted_id})
