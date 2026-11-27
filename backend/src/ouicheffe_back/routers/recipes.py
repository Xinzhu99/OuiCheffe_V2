from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ouicheffe_back.schema.schema import TagResponse
from ouicheffe_back.services.tags import TagsService, get_tag_service

recipe_router = APIRouter(
    prefix="/recipes/:id",
    tags=["recipe-detail"],
)

@recipe_router.get("",response_model=list[TagResponse])
async def get_recipe(service: TagsService = Depends(get_tag_service)):
    return await service.get_all_tags()