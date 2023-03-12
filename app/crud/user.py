from typing import Any
from app.crud.base import CRUD
from pymongo.collection import Collection
from app.core.security import get_password_hash, verify_password


class CrudUsers(CRUD):
    """
    Note that no validation is performed on the data, it is assumed that the data is valid
    """
    @staticmethod
    def read_by_email(collection: Collection, *, email: str) -> dict or None:
        """
        :return: user if found, None otherwise
        """
        return collection.find_one({"email": email})

    def authenticate(self, collection: Collection, *, email: str, password: str) -> dict or None:
        """
        :return: user if found and password is correct, None otherwise
        """
        user = self.read_by_email(collection=collection,
                                  email=email)

        if user is None or verify_password(plain_password=password,
                                           hashed_password=user.get("password")) is False:
            return None

        return user

    def create(self, collection: Collection, *, obj_in: dict) -> dict:
        obj_in["password"] = get_password_hash(obj_in.get("password"))
        obj_in["is_active"] = True
        obj_in["is_superuser"] = False

        return super().create(collection=collection,
                              obj_in=obj_in)

    def update(self, collection: Collection, *, _id: Any, obj_in: dict) -> dict or None:
        obj_in["password"] = get_password_hash(obj_in.get("password"))

        return super().update(collection=collection,
                              _id=_id,
                              obj_in=obj_in)


users = CrudUsers()
