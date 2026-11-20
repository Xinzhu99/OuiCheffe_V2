from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from ouicheffe_back.db.database import get_async_session
from ouicheffe_back.models import Tag
from ouicheffe_back.repositories.base import BaseRepository



class TagsRepository(BaseRepository):

    async def get_all_tags(self) -> list[Tag]:
        stmt = select(Tag).order_by(Tag.id)
        result = await self.session.execute(stmt)
        # pas besoin de dict() : from_attributes=True dans le schéma lit directement les objets SQLAlchemy
        return list(result.unique().scalars().all())


async def get_tag_repository(session: AsyncSession = Depends(get_async_session)) -> TagsRepository:
    return TagsRepository(session)
