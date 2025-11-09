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


class TagBase(BaseModel):
    name: str
    slug: str


class TagRead(TagBase):
    id: int


class TagCreate(TagBase):
    pass
