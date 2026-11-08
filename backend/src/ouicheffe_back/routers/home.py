from fastapi import APIRouter, Depends
from ouicheffe_back.schema.schema import RecipesResponse
from ouicheffe_back.services.recipes import RecipesService, get_recipe_service

home_router = APIRouter(
    prefix="",
    tags=["home"],
)


# liste vide -> 200 avec [] (pas 404 : la route existe, il n'y a juste pas encore de recettes)
@home_router.get("/", response_model=list[RecipesResponse])
async def get_recipes(service: RecipesService = Depends(get_recipe_service)):
    return await service.get_all_recipes()
