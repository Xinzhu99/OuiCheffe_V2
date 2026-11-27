from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ouicheffe_back.db.database import get_async_session
from ouicheffe_back.models import Recipe, RecipeIngredient   
from ouicheffe_back.repositories.base import BaseRepository


class RecipeDetailsRepository(BaseRepository):

    async def get_recipe(self, recipe_id: int) -> Recipe | None:   
        stmt = (
            select(Recipe)
            .where(Recipe.id == recipe_id)
            .options(
                selectinload(Recipe.tags),
                selectinload(Recipe.instructions),
                # 2 étages : les lignes (quantity) PUIS l'ingrédient de chaque ligne
                selectinload(Recipe.ingredients).selectinload(RecipeIngredient.ingredient),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()   # ✏️ parenthèses : on appelle la fonction


async def get_recipe_details_repository(session: AsyncSession = Depends(get_async_session)) -> RecipeDetailsRepository:
    return RecipeDetailsRepository(session)