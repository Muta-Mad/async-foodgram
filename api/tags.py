from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import get_db

from .models import Tag
from .schemas import TagBase

router = APIRouter(prefix='/tags', tags=['Tags'])


async def get_all_tags(session: AsyncSession):
    stmt = select(Tag).order_by(Tag.id)
    result = await session.scalars(stmt)
    return result.all()

@router.get('/', response_model=list[TagBase])
async def get_tags(session: AsyncSession = Depends(get_db)):
    tags = await get_all_tags(session=session)
    return tags
