from app.crud.user import users
from app.core.utils import get_response
from fastapi.encoders import jsonable_encoder
from app.api.deps import get_current_active_superuser
from app.schemas.user import User, UserCreate, UserUpdate
from fastapi import APIRouter, Request, status, HTTPException, Depends

router = APIRouter()
collection_name = "users"
superuser_access = Depends(get_current_active_superuser)


@router.post(path="/",
             response_model=User,
             responses={status.HTTP_400_BAD_REQUEST: get_response(description="Bad Request",
                                                                  message="Email already registered")},
             status_code=status.HTTP_201_CREATED)
def create(request: Request, user: UserCreate) -> User:
    """
    create a new user
    """
    db = request.app.database[collection_name]
    user = jsonable_encoder(user)

    if users.read_by_email(collection=db,
                           email=user.get("email")) is not None:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")

    created_user = users.create(collection=db,
                                obj_in=user)

    return User(**created_user)


@router.get(path="/{user_id}",
            response_model=User,
            responses={status.HTTP_404_NOT_FOUND: get_response(description="Not Found",
                                                               message="User not found")},
            status_code=status.HTTP_200_OK)
def read(request: Request, _id: str, superuser: User = superuser_access) -> User:
    """
    get a user by id
    """
    db = request.app.database[collection_name]
    user = users.read_one(collection=db,
                          _id=_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    return User(**user)


@router.put(path="/{user_id}",
            response_model=User,
            responses={status.HTTP_404_NOT_FOUND: get_response(description="Not Found",
                                                               message="User not found")},
            status_code=status.HTTP_200_OK)
def update(request: Request, _id: str, new_user_version: UserUpdate, superuser: User = superuser_access) -> User:
    """
    update a user by id
    """
    db = request.app.database[collection_name]
    user = users.read_one(collection=db,
                          _id=_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    updated_user = users.update(collection=db,
                                _id=_id,
                                obj_in=new_user_version)

    return User(**updated_user)


@router.delete(path="/{user_id}",
               response_model=User,
               responses={status.HTTP_404_NOT_FOUND: get_response(description="Not Found",
                                                                  message="User not found")},
               status_code=status.HTTP_200_OK)
def delete(request: Request, _id: str, superuser: User = superuser_access) -> User:
    """
    delete a user by id
    """
    db = request.app.database[collection_name]
    user = users.read_one(collection=db,
                          _id=_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    deleted_user = users.delete(collection=db,
                                _id=_id)

    return User(**deleted_user)
