from models.tag import Tag
from services.base_service import BaseService
from schemas.tag import TagCreate, TagUpdate
from repositories.tag_repository import TagRepository


class TagService(BaseService[Tag, TagCreate, TagUpdate, TagRepository]):

    def __init__(self):
        repository = TagRepository()
        super().__init__(repository)
