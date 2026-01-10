from pydantic import BaseModel

from api.users.schemas import UserRead

class IngredientInRecipe(BaseModel):
    id: int
    name: str
    measurement_unit: str
    amount: int

class IngredientInRecipeCreate(BaseModel):
    id: int
    amount: int

class RecipeRead(BaseModel):
    id: int
    tags: list['TagRead']
    author: UserRead
    ingredients: list[IngredientInRecipe]
    name: str
    image: str | None = None
    text: str
    cooking_time: int


class RecipeCreate(BaseModel):
    ingredients: list['IngredientInRecipeCreate']
    tags: list[int]
    image: str | None = None
    name: str
    text: str
    cooking_time: int



class TagRead(BaseModel):
    id: int
    name: str
    slug: str
