from fastapi import APIRouter, Depends, HTTPException, status
from ouicheffe_back.auth.dependencies import get_current_user
from ouicheffe_back.schema.schema import UserResponse, RegisterUserSchema
from ouicheffe_back.services.users import UserService, get_user_service

home_router = APIRouter(
    prefix="",
    tags=["home"],
)


@home_router.get("/")
async def get_home():
    return {"message": "Welcome to the Home Page"}

