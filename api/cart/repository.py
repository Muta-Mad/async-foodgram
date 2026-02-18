from sqlalchemy import select

from api.cart.schemas import RecipeShort
from api.cart.models import ShoppingCart
from api.recipes.models import Recipe


def get_shopping_cart_query(id, current_user):
    return select(ShoppingCart).where(ShoppingCart.recipe_id == id, ShoppingCart.user_id == current_user.id)

def get_recipe(recipe_id):
    return select(Recipe).where(Recipe.id == recipe_id)

def short_recipe(recipe):
    return RecipeShort(
        id=recipe.id,
        name=recipe.name,
        image=recipe.image,
        cooking_time=recipe.cooking_time
    )
