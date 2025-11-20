from models.user import User
from repositories.base_repository import BaseRepository
from schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    
    def __init__(self):
        super().__init__(User)
