from bson import ObjectId
from typing import Optional
from app.core.utils import PyObjectId
from pydantic import BaseModel, Field, EmailStr


# Properties to receive via API on creation
class UserCreate(BaseModel):
    email: EmailStr = Field(...)
    pseudo: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "email@email.com",
                "pseudo": "pseudo",
                "password": "password"
            }
        }


# Properties to receive via API on update
class UserUpdate(BaseModel):
    pseudo: Optional[str] = None
    password: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "pseudo": "pseudo",
                "password": "password"
            }
        }


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    pseudo: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


class UserInDBBase(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId,
                           alias="_id")


# Additional properties to return via API
class User(UserInDBBase):
    pass

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "email@email.com",
                "pseudo": "pseudo",
                "is_active": True,
                "is_superuser": False,
                "_id": "60a9b4f8f9f2b5b2b8e1f2f5"
            }
        }


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str
