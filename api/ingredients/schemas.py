from pydantic import BaseModel


class IngredientRead(BaseModel):
    id: int
    name: str
    measurement_unit: str
