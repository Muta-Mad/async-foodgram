from pydantic import BaseModel


class RecipeShort(BaseModel):
    id: int
    name: str
    image: str | None = None
    cooking_time: int
