from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str
    measurement_unit: str


class IngredientRead(IngredientBase):
    id: int


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    pass
