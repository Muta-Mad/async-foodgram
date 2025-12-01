from pydantic import BaseModel


class TagRead(BaseModel):
    id: int
    name: str
    slug: str
