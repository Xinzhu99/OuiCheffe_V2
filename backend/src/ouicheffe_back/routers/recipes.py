from fastapi import APIRouter, Depends, HTTPException, status   # ✏️ HTTPException + status
from ouicheffe_back.schema.schema import RecipeDetailsResponse
from ouicheffe_back.services.recipe_details import RecipeDetailsService, get_recipe_details_service

recipe_router = APIRouter(
    prefix="/recipe",
    tags=["recipe-details"],
)

@recipe_router.get("/{recipe_id}", response_model=RecipeDetailsResponse)   
async def get_recipe_details(
    recipe_id: int,                    
    service: RecipeDetailsService = Depends(get_recipe_details_service),
):
    recipe = await service.get_recipe(recipe_id)
    if recipe is None:                  # ✏️ recette introuvable → 404 au lieu d'une erreur 500
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recette introuvable")
    return recipe