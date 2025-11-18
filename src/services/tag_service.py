from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.tag import Tag
# from repositories.tag_repository import TagRepository


class TagService:

    # def create_tag(self, db, user_data: TagCreate) -> Tag:
    #     return self.user_repository.create(db, user_data)

    async def get_all_tags(self, session: AsyncSession):
        stmt = select(Tag).order_by(Tag.id)
        result = await session.scalars(stmt)
        return result.all()

    async def get_tag(self, session: AsyncSession, id: int):
        stmt = select(Tag).where(Tag.id == id)
        result = await session.scalar(stmt)
        return result
