from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from api.tags.models import Tag
from api.tags.schemas import TagRead
from api.example.tag_repository import TagRepository
from api.example.tag_service import TagService
from api.core.exceptions import NotFoundException

router = APIRouter(prefix='/example', tags=['Example'])


def get_tag_repository(
    session: AsyncSession = Depends(get_db)
) -> TagRepository:
    return TagRepository(session=session)


def get_tag_service(
    repository: TagRepository = Depends(get_tag_repository)
) -> TagService:
    return TagService(repository)


@router.get('/', response_model=list[TagRead])
async def get_all_tags(
    service: TagService = Depends(get_tag_service)
) -> list[Tag]:
    """get - запрос для получения списка тегов"""
    tags = await service.get_all()
    return tags


@router.get('/{id}', response_model=TagRead)
async def get_tag(
    id: int,
    service: TagService = Depends(get_tag_service)
) -> Tag | None:
    """get - запрос для получения объекта тега по id"""
    try:
        tag = await service.get_object(id)
        return tag
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tag с таким ID не существует.',
        )
