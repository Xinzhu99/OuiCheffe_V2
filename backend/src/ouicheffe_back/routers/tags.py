from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ouicheffe_back.schema.schema import TagResponse
from ouicheffe_back.services.tags import TagsService, get_tag_service

tag_router = APIRouter(
    prefix="/tags",
    tags=["tags"],
)

@tag_router.get("/",response_model=list[TagResponse])
async def get_tags(service: TagsService = Depends(get_tag_service)):
    return await service.get_all_tags()