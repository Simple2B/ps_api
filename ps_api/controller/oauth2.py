from datetime import datetime, timedelta, UTC
from fastapi import status
from jose import JWTError, jwt
from fastapi import HTTPException
from pydantic import ValidationError

from ps_api import schema as s
from ps_api.config import CFG

INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: s.TokenData) -> str:
    data.exp = datetime.now(UTC) + timedelta(minutes=CFG.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.model_dump()
    encoded_jwt = jwt.encode(to_encode, CFG.SECRET_KEY)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> s.TokenData:
    try:
        payload = jwt.decode(token, CFG.SECRET_KEY)
        return s.TokenData.model_validate(payload)

    except (JWTError, ValidationError):
        raise credentials_exception
