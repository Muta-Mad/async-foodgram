from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schemas.tag import TagRead
from services.tag_service import TagService


router = APIRouter(prefix='/tags', tags=['Tags'])
tag_service = TagService()


@router.get('/', response_model=list[TagRead])
async def get_tags(session: AsyncSession = Depends(get_db)):
    tags = await tag_service.get_all_tags(session=session)
    return tags


@router.get('/{id}', response_model=TagRead)
async def get_tag(id: int, session: AsyncSession = Depends(get_db)):
    tag = await tag_service.get_tag(session, id)
    return tag
