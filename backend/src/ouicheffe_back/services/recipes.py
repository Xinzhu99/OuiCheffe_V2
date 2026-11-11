from fastapi import Depends

from ouicheffe_back.models import Recipe
from ouicheffe_back.repositories.recipes import RecipesRepository, get_recipe_repository


class RecipesService:
    def __init__(self, recipe_repo: RecipesRepository):
        self.recipe_repo = recipe_repo

    async def get_all_recipes(self) -> list[Recipe]:
        return await self.recipe_repo.get_all_recipes()
    


async def get_recipe_service(recipe_repo: RecipesRepository = Depends(get_recipe_repository)) -> RecipesService:
    return RecipesService(recipe_repo)
