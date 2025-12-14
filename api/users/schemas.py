from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str 
    first_name: str 
    last_name: str 
    avatar: str | None = None 


class UserCreate(schemas.BaseUserCreate, UserBase):
    pass


class UserRead(UserBase):
    id: int
    is_subscribed: bool = False
