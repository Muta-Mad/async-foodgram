from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str 
    first_name: str 
    last_name: str 
    avatar: str | None = None 


class UserResponse(UserBase):
    id: int
    is_subscribed: bool = False


class UserBaseUpdate(UserBase):
    email: EmailStr | None = None 
    username: str | None = None 
    first_name: str | None = None 
    last_name: str | None = None 
    avatar: str | None = None 


class UserCreate(schemas.BaseUserCreate, UserBase):
    pass


class UserRead(schemas.BaseUser[int], UserBase):
    is_subscribed: bool = False


class UserUpdate(schemas.BaseUserUpdate, UserBaseUpdate):
    pass