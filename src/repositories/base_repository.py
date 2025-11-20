from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, TypeVar, Generic, Type
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый репозиторий с CRUD операциями."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, session: AsyncSession, id: int) -> Optional[ModelType]:
        """Получить объект по ID."""
        stmt = select(self.model).where(self.model.id == id)
        result = await session.scalar(stmt)
        return result

    async def get_all(self, session: AsyncSession) -> List[ModelType]:
        """Получить все объекты."""
        stmt = select(self.model)
        result = await session.scalars(stmt)
        return result.all()

    async def create(
        self,
        session: AsyncSession,
        obj_in: CreateSchemaType | dict
    ) -> ModelType:
        """Создать новый объект."""
        db_obj = self.model(**obj_in.model_dump())
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        id: int,
        obj_in: UpdateSchemaType | dict
    ) -> Optional[ModelType]:
        """Обновить объект."""
        update_data = obj_in.obj_in.model_dump(exclude_unset=True)

        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
            .returning(self.model)
        )
        result = await session.scalar(stmt)
        await session.commit()
        return result

    async def delete(self, session: AsyncSession, id: int) -> bool:
        """Удалить объект."""
        stmt = delete(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0
