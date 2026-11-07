from typing import Dict
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from ouicheffe_back.db.database import get_async_session
from ouicheffe_back.models.models import Brigade, User
from ouicheffe_back.repositories.base import BaseRepository
from ouicheffe_back.utils.exceptions import UserAlreadyExistsException


class UserRepository(BaseRepository):

  async def get_by_email(self, email: str) -> User | None:
        try:
            stmt = select(User).filter_by(email=email)
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except SQLAlchemyError:
            return None


  async def create(self, data: Dict) -> User | None:
    brigade = Brigade()
    self.session.add(brigade)
    await self.session.flush()                  # brigade.id is set, nothing committed yet

    user = User(**data, brigade_id=brigade.id)
    self.session.add(user)
    try:
        await self.session.commit()             # brigade + user together
    except IntegrityError as exc:               # e.g. two sign-ups with the same email at the same time
        await self.session.rollback()           # the brigade is cancelled too
        raise UserAlreadyExistsException(data["email"]) from exc
    await self.session.refresh(user)
    return user

async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)