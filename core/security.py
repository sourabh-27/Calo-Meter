from datetime import datetime, timedelta
from typing import Any, Union
import os
import schemas
from functools import wraps
import jwt
import os
import json
from fastapi.responses import JSONResponse
from jose import jwt
from passlib.context import CryptContext
from .config import settings
import base64

from fastapi import Depends, HTTPException, Security
from starlette import status
from .api_key import APIKeyHeader
# from fastapi.security.api_key import APIKeyHeader

from dotenv import load_dotenv
load_dotenv()
api_key_header_auth = APIKeyHeader(name=os.getenv("API_KEY_NAME"), auto_error=True)
async def get_api_key(api_key_header: str = Security(api_key_header_auth)):
    if api_key_header != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def encode_user_id(
    subject: Union[str, Any]
) -> str:
    to_encode = {"sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY_CM, algorithm=ALGORITHM)
    return encoded_jwt

def decode_user_id(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY_CM, algorithms=[ALGORITHM])
    token_data = schemas.TokenPayload(**payload)
    return token_data.sub

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            jwt_encoded_token = kwargs.get('request').cookies.get('jwt_token')
            try:
                jwt.decode(jwt_encoded_token, os.getenv("AUTH_SECRET_KEY"))
            except:
                return JSONResponse(content = {"error": "Unauthorized"}, status_code=401)
            else:
                return fn(*args, **kwargs)

        return decorator

    return wrapper