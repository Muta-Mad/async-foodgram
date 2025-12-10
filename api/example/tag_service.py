from api.example.tag_repository import TagRepository
from api.core.base_service import BaseService


class TagService(BaseService):
    """Сервис для Tags."""

    def __init__(self, repository: TagRepository):
        self.repository = repository
