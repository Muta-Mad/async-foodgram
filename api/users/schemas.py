from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field

from api.users.validators import USERNAME


class UserBase(BaseModel):
    email: EmailStr = Field(max_length=254)
    username: USERNAME
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)


class UserCreate(schemas.BaseUserCreate, UserBase):
    pass


class UserResponce(UserBase):
    id: int


class UserRead(UserBase):
    id: int
    is_subscribed: bool = False
    avatar: str | None = None 

class EmailPassword(BaseModel):
    email: EmailStr
    password: str
