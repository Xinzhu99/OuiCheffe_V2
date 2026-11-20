from fastapi import Depends

from ouicheffe_back.models import Tag
from ouicheffe_back.repositories.tags import TagsRepository, get_tag_repository


class TagsService:
    def __init__(self, tag_repo: TagsRepository):
        self.tag_repo = tag_repo

    async def get_all_tags(self) -> list[Tag]:
        return await self.tag_repo.get_all_tags()
    


async def get_tag_service(tag_repo: TagsRepository = Depends(get_tag_repository)) -> TagsService:
    return TagsService(tag_repo)
