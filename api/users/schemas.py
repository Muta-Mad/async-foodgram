from fastapi_users import schemas
from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    avatar: str | None = None


class UserBaseUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None


class UserCreate(schemas.BaseUserCreate, UserBase):
    pass


class UserRead(schemas.BaseUser[int], UserBase):
    pass


class UserUpdate(schemas.BaseUserUpdate, UserBaseUpdate):
    pass