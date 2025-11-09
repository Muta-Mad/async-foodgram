from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import get_db

from .models import Tag
from .schemas import TagRead, TagCreate

router = APIRouter(prefix='/tags', tags=['Tags'])


async def post_create_tag(
    session: AsyncSession,
    tag_create: TagCreate,
    ) -> Tag:
    """ Создание тега в БД."""

    tag = Tag(**tag_create.model_dump())
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag


async def get_all_tags(session: AsyncSession):
    stmt = select(Tag).order_by(Tag.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_tag_object(session: AsyncSession, id: int):
    stmt = select(Tag).where(Tag.id == id)
    result = await session.scalar(stmt)
    return result

@router.get('/', response_model=list[TagRead])
async def get_tags(session: AsyncSession = Depends(get_db)):
    tags = await get_all_tags(session=session)
    return tags

@router.get('/{id}', response_model=TagRead)
async def get_tag(id: int, session: AsyncSession = Depends(get_db)):
    tag = await get_tag_object(session, id)
    return tag


@router.post('/', response_model=TagCreate)
async def create_tag(
    tag_data: TagCreate,
    session: AsyncSession = Depends(get_db),
    ):
    tag = await post_create_tag(session, tag_create=tag_data)
    return tag
