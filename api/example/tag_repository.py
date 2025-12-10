from sqlalchemy.ext.asyncio import AsyncSession

from api.tags.models import Tag
from api.core.base_repository import BaseRepository


class TagRepository(BaseRepository):
    """Репозиторий для Tag."""

    def __init__(self, session: AsyncSession):
        self.model = Tag
        self.session = session
