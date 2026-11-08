from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ouicheffe_back.db.database import get_async_session
from ouicheffe_back.models import Recipe
from ouicheffe_back.repositories.base import BaseRepository


class RecipesRepository(BaseRepository):

    async def get_all_recipes(self) -> list[Recipe]:
        # pas de try/except : une erreur de BDD doit remonter en 500, pas passer pour "aucune recette"
        stmt = select(Recipe).order_by(Recipe.id)
        result = await self.session.execute(stmt)
        # pas besoin de dict() : from_attributes=True dans le schéma lit directement les objets SQLAlchemy
        return list(result.scalars().all())


async def get_recipe_repository(session: AsyncSession = Depends(get_async_session)) -> RecipesRepository:
    return RecipesRepository(session)
