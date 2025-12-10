from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from api.basemodel import Base


class BaseRepository:
    """Базовый репозиторий с CRUD операциями."""

    def __init__(self, model: Base, session: AsyncSession):
        self.model = model
        self.session = session

    async def get_object(self, id: int) -> Base | None:
        """Получить объект по ID."""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.scalar(stmt)
        return result

    async def get_all(self) -> list[Base]:
        """Получить все объекты."""
        stmt = select(self.model)
        result = await self.session.scalars(stmt)
        return result.all()

    async def create(self, obj_in: BaseModel) -> Base:
        """Создать новый объект."""
        db_obj = self.model(**obj_in.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, id: int, obj_in: BaseModel) -> Base | None:
        """Обновить объект."""
        update_data = obj_in.obj_in.model_dump(exclude_unset=True)

        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
            .returning(self.model)
        )
        result = await self.session.scalar(stmt)
        await self.session.commit()
        return result

    async def delete(self, id: int) -> bool:
        """Удалить объект."""
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
