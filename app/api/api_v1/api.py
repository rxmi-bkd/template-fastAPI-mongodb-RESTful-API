from fastapi import APIRouter
from app.api.api_v1.endpoints import auth
from app.api.api_v1.endpoints import user

api_router = APIRouter()


api_router.include_router(router=auth.router,
                          prefix="/auth",
                          tags=["auth"])

api_router.include_router(router=user.router,
                          prefix="/user",
                          tags=["user"])
