from models.ingredient import Ingredient
from repositories.base_repository import BaseRepository
from schemas.ingredient import IngredientCreate, IngredientUpdate


class IngredientRepository(
    BaseRepository[Ingredient, IngredientCreate, IngredientUpdate]
):
    
    def __init__(self):
        super().__init__(Ingredient)
