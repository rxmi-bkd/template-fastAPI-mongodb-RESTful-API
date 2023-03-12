from datetime import timedelta
from app.crud.user import users
from app.core.config import CONFIG
from app.schemas.token import Token
from app.core.utils import get_response
from app.core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Request, HTTPException, status, Depends

router = APIRouter()
collection_name = "users"


@router.post(path="/access-token",
             response_model=Token,
             responses={status.HTTP_401_UNAUTHORIZED: get_response(description="Unauthorized",
                                                                   message="Incorrect email or password")},
             status_code=status.HTTP_200_OK)
def get_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    get an access token to authenticate the user
    """
    user = users.authenticate(collection=request.app.database[collection_name],
                              email=form_data.username,
                              password=form_data.password)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")

    if user.get("is_active") is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Inactive user")

    access_token_expires = timedelta(minutes=CONFIG.access_token_lifetime)

    return Token(access_token=create_access_token(subject=user.get("_id"),
                                                  expires_delta=access_token_expires),
                 token_type="bearer")
