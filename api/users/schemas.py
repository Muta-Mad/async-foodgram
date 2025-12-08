from fastapi_users import schemas
from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    avatar: str | None = None


class UserRead(UserBase, schemas.BaseUser[int]):
    pass


class UserCreate(UserBase, schemas.BaseUserCreate):
    pass


class UserUpdate(UserBase, schemas.BaseUserUpdate):
    pass