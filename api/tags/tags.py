from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db

from api.tags.models import Tag
from api.tags.schemas import TagRead

router = APIRouter(prefix='/tags', tags=['Tags'])


async def get_all_tags(session: AsyncSession):
    stmt = select(Tag).order_by(Tag.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_tag_object(session: AsyncSession, id: int):
    stmt = select(Tag).where(Tag.id == id)
    result = await session.scalar(stmt)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Тега с таким ID не существует.'
        )
    return result

@router.get('/', response_model=list[TagRead])
async def get_tags(session: AsyncSession = Depends(get_db)):
    tags = await get_all_tags(session=session)
    return tags

@router.get('/{id}', response_model=TagRead)
async def get_tag(id: int, session: AsyncSession = Depends(get_db)):
    tag = await get_tag_object(session, id)
    return tag
