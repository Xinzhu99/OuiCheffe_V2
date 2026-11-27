from fastapi import Depends
from ouicheffe_back.models import Recipe
from ouicheffe_back.repositories.recipe_details import RecipeDetailsRepository, get_recipe_details_repository


class RecipeDetailsService:
    def __init__(self, recipe_details_repo: RecipeDetailsRepository):
        self.recipe_details_repo = recipe_details_repo

    async def get_recipe(self, recipe_id: int) -> Recipe | None:   # ✏️
        return await self.recipe_details_repo.get_recipe(recipe_id)


async def get_recipe_details_service(
    recipe_details_repo: RecipeDetailsRepository = Depends(get_recipe_details_repository),
) -> RecipeDetailsService:
    return RecipeDetailsService(recipe_details_repo)