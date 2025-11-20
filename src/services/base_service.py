from typing import Generic, TypeVar, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from repositories.base_repository import BaseRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseService(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, RepositoryType]
):
    """Базовый сервис с общей бизнес-логикой."""

    def __init__(self, repository: RepositoryType):
        self.repository = repository

    async def get(self, session: AsyncSession, id: int) -> ModelType:
        """Получить объект по ID с обработкой ошибки 404."""
        obj = await self.repository.get(session, id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Объект с id {id} не найден"
            )
        return obj

    async def get_all(self, session: AsyncSession) -> List[ModelType]:
        """Получить все объекты."""
        return await self.repository.get_all(session)

    async def create(
        self, session: AsyncSession, obj_in: CreateSchemaType
    ) -> ModelType:
        """Базовое создание объекта"""
        return await self.repository.create(session, obj_in)

    async def update(
        self,
        session: AsyncSession,
        id: int,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        """Базовое обновление объекта."""
        await self.get(session, id)
        return await self.repository.update(session, id, obj_in)

    async def delete(self, session: AsyncSession, id: int) -> bool:
        """Удалить объект."""
        await self.get(session, id)
        return await self.repository.delete(session, id)
