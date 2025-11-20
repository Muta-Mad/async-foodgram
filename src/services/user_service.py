from models.user import User
from services.base_service import BaseService
from schemas.user import UserCreate, UserUpdate
from repositories.user_repository import UserRepository


class UserService(BaseService[User, UserCreate, UserUpdate, UserRepository]):
    
    def __init__(self):
        repository = UserRepository()
        super().__init__(repository)
