from jose import jwt
from app.crud.user import users
from app.schemas.user import User
from app.core.config import CONFIG
from pydantic import ValidationError
from app.core.security import ALGORITHM
from app.schemas.token import TokenPayload
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{CONFIG.base_url}/auth/access-token")


def get_current_user(request: Request, token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token=token,
                             key=CONFIG.secret_key,
                             algorithms=[ALGORITHM])

        token_data = TokenPayload(**payload)

    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Could not validate credentials")

    collection = request.app.database['users']  # collection/table that contains users
    user = users.read_one(collection=collection,
                          _id=token_data.sub)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    return User(**user)


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:

    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")

    return current_user


def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:

    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You don't have enough privileges")

    return current_user
