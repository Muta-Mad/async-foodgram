from pydantic import BaseModel


class TagBase(BaseModel):
    name: str
    slug: str


class TagRead(TagBase):
    id: int


class TagCreate(TagBase):
    pass


class TagList(BaseModel):
    users: list[TagRead]
