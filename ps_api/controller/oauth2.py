from datetime import datetime, timedelta, UTC

from bson.objectid import ObjectId
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from pymongo.database import Database

from ps_api import schema as s
from ps_api import model as m
from ps_api.config import CFG
from ps_api.database import get_db

INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def create_access_token(data: s.TokenData) -> str:
    data.exp = datetime.now(UTC) + timedelta(minutes=CFG.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.model_dump()
    encoded_jwt = jwt.encode(to_encode, CFG.SECRET_KEY)
    return encoded_jwt


def verify_access_token(token: str) -> s.TokenData:
    try:
        payload = jwt.decode(token, CFG.SECRET_KEY)
        return s.TokenData.model_validate(payload)

    except (JWTError, ValidationError):
        raise INVALID_CREDENTIALS_EXCEPTION


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Database = Depends(get_db),
) -> m.User:
    token_data: s.TokenData = verify_access_token(token)

    if token_data.user_id is not None:
        return m.User.model_validate(db.users.find_one({"_id": ObjectId(token_data.user_id)}))
    else:
        raise INVALID_CREDENTIALS_EXCEPTION
