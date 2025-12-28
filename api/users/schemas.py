from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field

from api.users.validators import USERNAME


class UserBase(BaseModel):
    """Базовая схема пользователей"""
    email: EmailStr = Field(max_length=254)
    username: USERNAME
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)


class UserCreate(schemas.BaseUserCreate, UserBase):
    """Схема для создания пользователя"""
    pass


class UserResponce(UserBase):
    """Схема ответа для пользователя"""
    id: int


class UserRead(UserBase):
    """Схема ответа для списка пользователей"""
    id: int
    is_subscribed: bool = False
    avatar: str | None = None 

class EmailPassword(BaseModel):
    """Схема для получение токена"""
    email: EmailStr
    password: str

class Avatar(BaseModel):
    """Схема для загрузки аватара в Base64"""
    avatar: str

class SetPassword(BaseModel):
    """Схема для замены пароля"""
    new_password: str = Field(min_length=8)
    current_password: str