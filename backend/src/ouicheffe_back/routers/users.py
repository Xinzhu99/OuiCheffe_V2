from fastapi import APIRouter, Depends, HTTPException, status
from ouicheffe_back.auth.dependencies import get_current_user
from ouicheffe_back.schema.schema import UserResponse, RegisterUserSchema
from ouicheffe_back.services.users import UserService, get_user_service

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.post("/", response_model=UserResponse)
async def create(user: RegisterUserSchema,
        service: UserService = Depends(get_user_service)):
    new_user = await service.register(user)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    return new_user


@user_router.get("/get/me/", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return current_user