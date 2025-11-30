from pydantic import BaseModel


class UserBase(BaseModel):
    """Базовая схема пользователя."""
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    """Схема создания пользователя."""
    pass


class UserRead(UserBase):
    """Схема чтения данных пользователя."""
    id: int
    pass
