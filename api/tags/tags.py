from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from api.tags.models import Tag
from api.tags.schemas import TagRead
from api.exceptions import not_found_error

router = APIRouter(prefix='/tags', tags=['Tags'])


async def get_all_tags(session: AsyncSession) -> list[Tag]:
    """Логика, возвращающая список тегов"""
    stmt = select(Tag).order_by(Tag.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_tag_object(session: AsyncSession, id: int) -> Tag|None:
    """Логика, возвращающая объект тега по id"""
    stmt = select(Tag).where(Tag.id == id)
    result = await session.scalar(stmt)
    if not result:
        not_found_error('Тег')
    return result


@router.get('/', response_model=list[TagRead])
async def get_tags(session: AsyncSession = Depends(get_db)) -> list[Tag]:
    """get - запрос для получения списка тегов"""
    tags = await get_all_tags(session=session)
    return tags


@router.get('/{id}', response_model=TagRead)
async def get_tag(
    id: int,
    session: AsyncSession = Depends(get_db),
) -> Tag | None:
    """get - запрос для получения объекта тега по id"""
    tag = await get_tag_object(session, id)
    return tag
