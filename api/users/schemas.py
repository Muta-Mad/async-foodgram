from fastapi_users import schemas
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str 
    first_name: str 
    last_name: str 
    avatar: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str


class UserBaseUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None


class UserCreate(schemas.BaseUserCreate, UserBase):
    pass


class UserRead(schemas.BaseUser[int], UserBase):
    is_subscribed: bool = False


class UserUpdate(schemas.BaseUserUpdate, UserBaseUpdate):
    pass