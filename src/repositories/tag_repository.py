from models.tag import Tag
from repositories.base_repository import BaseRepository
from schemas.tag import TagCreate, TagUpdate


class TagRepository(BaseRepository[Tag, TagCreate, TagUpdate]):

    def __init__(self):
        super().__init__(Tag)
