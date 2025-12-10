from pydantic import BaseModel

from api.core.base_repository import BaseRepository
from api.basemodel import Base
from api.core.exceptions import NotFoundException


class BaseService:
    """Базовый сервис с общей бизнес-логикой."""

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def get_object(self, id: int) -> Base | None:
        """Получить объект по ID с обработкой ошибки."""
        obj = await self.repository.get_object(id)
        if not obj:
            raise NotFoundException
        return obj

    async def get_all(self) -> list[Base]:
        """Получить все объекты."""
        return await self.repository.get_all()

    async def create(self, obj_in: BaseModel) -> Base:
        """Базовое создание объекта."""
        return await self.repository.create(obj_in)

    async def update(self, id: int, obj_in: BaseModel) -> Base:
        """Базовое обновление объекта."""
        await self.get(id)
        return await self.repository.update(id, obj_in)

    async def delete(self, id: int) -> bool:
        """Удалить объект."""
        await self.get(id)
        return await self.repository.delete(id)
