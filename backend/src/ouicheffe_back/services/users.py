from fastapi import Depends

from ouicheffe_back.models import User
from ouicheffe_back.schema.schema import RegisterUserSchema, UserResponse
from ouicheffe_back.repositories.users import UserRepository, get_user_repository
from ouicheffe_back.utils.utils import get_hashed_password
from ouicheffe_back.utils.exceptions import UserAlreadyExistsException

class UserService:
    def __init__(self, user_repo: UserRepository = Depends(get_user_repository)):
        self.user_repo = user_repo

    async def register(self, data: RegisterUserSchema) -> User:
        if await self.user_repo.get_by_email(data.email):
            raise UserAlreadyExistsException(data.email)
        user_dict = data.model_dump(exclude={"password"})
        user_dict["hashed_password"] = get_hashed_password(data.password)
        return await self.user_repo.create(user_dict)


    async def get_by_email(self, email: str) -> User | None:
        return await self.user_repo.get_by_email(email)


async def get_user_service(repo: UserRepository = Depends(get_user_repository)):
    return UserService(repo)