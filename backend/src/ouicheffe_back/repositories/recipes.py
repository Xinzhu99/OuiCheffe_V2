from fastapi import Depends
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from ouicheffe_back.db.database import get_async_session
from ouicheffe_back.models import Recipe, Tag, Instruction
from ouicheffe_back.repositories.base import BaseRepository



class RecipesRepository(BaseRepository):

    async def get_all_recipes(self, tag_id: int |None = None, search: str | None = None,) -> list[Recipe]:
        # pas de try/except : une erreur de BDD doit remonter en 500, pas passer pour "aucune recette"
        stmt = select(Recipe).options(joinedload(Recipe.tags)).order_by(Recipe.id)

        if tag_id is not None:
            stmt = stmt.where(Recipe.tags.any(Tag.id == tag_id))

        if search is not None:
            search = search.strip()
            if search :
                stmt = stmt.where(
                    or_(
                        Recipe.name.ilike(f"%{search}%"),
                        Recipe.instructions.any(Instruction.instruction.ilike(f"%{search}%"))
                        )
                )
                
        result = await self.session.execute(stmt)
        # pas besoin de dict() : from_attributes=True dans le schéma lit directement les objets SQLAlchemy
        return list(result.unique().scalars().all())


async def get_recipe_repository(session: AsyncSession = Depends(get_async_session)) -> RecipesRepository:
    return RecipesRepository(session)
