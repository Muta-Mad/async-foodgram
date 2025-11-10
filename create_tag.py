import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Tag
from database import engine, new_session, get_db


async def create_tag():
    async with new_session() as db:
        tag = Tag(
            name="Выпивка",
            slug="booze",
        )
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
        print(f'Тег создан с id {tag.id}')

asyncio.run(create_tag())
