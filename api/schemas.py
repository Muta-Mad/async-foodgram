from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    pass