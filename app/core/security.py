from jose import jwt
from typing import Any
from app.core.config import CONFIG
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")


def create_access_token(subject: str | Any, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=CONFIG.access_token_lifetime)

    to_encode = {"exp": expire,
                 "sub": str(subject)}

    encoded_jwt = jwt.encode(claims=to_encode,
                             key=CONFIG.secret_key,
                             algorithm=ALGORITHM)

    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=plain_password,
                              hash=hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
