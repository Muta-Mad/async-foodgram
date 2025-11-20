from models.ingredient import Ingredient
from services.base_service import BaseService
from schemas.ingredient import IngredientCreate, IngredientUpdate
from repositories.ingredient_repository import IngredientRepository


class IngredientService(
    BaseService[
        Ingredient,
        IngredientCreate,
        IngredientUpdate,
        IngredientRepository
    ]
):
    
    def __init__(self):
        repository = IngredientRepository()
        super().__init__(repository)
