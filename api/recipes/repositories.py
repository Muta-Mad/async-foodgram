from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.cart.models import ShoppingCart
from api.cart.schemas import RecipeShort
from api.core.exceptions import GlobalError
from api.favorite.models import Favorite
from api.recipes.models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag
from api.recipes.schemas import IngredientInRecipe, IngredientRead, RecipeRead, TagRead
from api.users.models import User
from api.users.schemas import UserRead


def map_recipe_to_read(
    recipe: Recipe,
    amount_map: dict[tuple[int, int], int],
    favorites_set: set[int],
    cart_set: set[int]
) -> RecipeRead:
    ingredients = [
        IngredientInRecipe(
            id=ingredient.id,
            name=ingredient.name,
            measurement_unit=ingredient.measurement_unit,
            amount=amount_map[(recipe.id, ingredient.id)],
        )
        for ingredient in recipe.ingredients
    ]
    is_favorited = recipe.id in favorites_set
    is_in_shopping_cart = recipe.id in cart_set
    tags = [map_tag_to_read(tag) for tag in recipe.tags]
    author = map_user_to_read(recipe.author)
    return RecipeRead(
        id=recipe.id,
        author=author,
        tags=tags,
        ingredients=ingredients,
        name=recipe.name,
        image=recipe.image,
        text=recipe.text,
        cooking_time=recipe.cooking_time,
        is_favorited=is_favorited,
        is_in_shopping_cart=is_in_shopping_cart,
    )

async def get_amount_map(
    session: AsyncSession,
    recipe_ids: list[int],
) -> dict[tuple[int, int], int]:
    if not recipe_ids:
        return {}
    result = await session.execute(
        select(RecipeIngredient)
        .where(RecipeIngredient.recipe_id.in_(recipe_ids))
    )
    return {
        (ri.recipe_id, ri.ingredient_id): ri.amount
        for ri in result.scalars()
    }

def get_recipes_query():
    return (
        select(Recipe)
        .options(
            selectinload(Recipe.author),
            selectinload(Recipe.tags),
            selectinload(Recipe.ingredients)
        )
        .order_by(Recipe.id)
    )

def get_recipe_query(id: int):
    return (
        select(Recipe)
        .options(
            selectinload(Recipe.author),
            selectinload(Recipe.tags),
            selectinload(Recipe.ingredients)
        )
        .where(Recipe.id==id)
    )

def map_user_to_read(user: User) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        is_subscribed=False,
        avatar=user.avatar,
    )

def map_tag_to_read(tag: Tag) -> TagRead:
    return TagRead(
            id=tag.id,
            name=tag.name,
            slug=tag.slug,
        )

def map_ingredient_to_read(ingredient: Ingredient) -> IngredientRead:
    return IngredientRead(
        id=ingredient.id,
        name=ingredient.name,
        measurement_unit=ingredient.measurement_unit
        )

async def build_recipe_read(
    session: AsyncSession,
    recipe: Recipe,
) -> RecipeRead:
    stmt = (
        select(Recipe)
        .where(Recipe.id == recipe.id)
        .options(
            selectinload(Recipe.author),
            selectinload(Recipe.tags),
            selectinload(Recipe.ingredients),
        )
    )
    result = await session.execute(stmt)
    recipe = result.scalar_one()
    amount_map = await get_amount_map(session, [recipe.id])
    return map_recipe_to_read(recipe, amount_map)

async def get_owned_recipe(
    session: AsyncSession,
    recipe_id: int,
    user_id: int,
) -> Recipe:
    query = (
    select(Recipe)
    .options(
        selectinload(Recipe.author),
        selectinload(Recipe.tags),
        selectinload(Recipe.ingredients),
    )
    .where(
        Recipe.id == recipe_id,
        Recipe.author_id == user_id
    )
    )
    result = await session.execute(query)
    recipe = result.scalar_one_or_none()
    if not recipe:
        GlobalError.not_found('Страница не найдена.')
    return recipe

def set_recipe_ingredients(
    recipe: Recipe,
    ingredients: list,
):
    recipe.recipe_ingredients.clear()
    recipe.recipe_ingredients.extend(
        RecipeIngredient(
            ingredient_id=item.id,
            amount=item.amount,
        )
        for item in ingredients
    )

def set_recipe_tags(
    recipe: Recipe,
    tags: list[int],
):
    recipe.recipe_tags.clear()
    recipe.recipe_tags.extend(
        RecipeTag(tag_id=tag_id)
        for tag_id in tags
    )

def short_recipe(recipe):
    return RecipeShort(
        id=recipe.id,
        name=recipe.name,
        image=recipe.image,
        cooking_time=recipe.cooking_time
    )


def get_tags_query():
    return select(Tag).order_by(Tag.id)

def get_tag_query(id):
    return select(Tag).where(Tag.id == id)

def get_ingredients_query():
    return select(Ingredient).order_by(Ingredient.id)

def get_ingredient_query(id):
    return select(Ingredient).where(Ingredient.id == id)

def get_recipe(recipe_id):
    return select(Recipe).where(Recipe.id == recipe_id)

def get_shopping_cart_query(id, current_user):
    return select(ShoppingCart).where(ShoppingCart.recipe_id == id, ShoppingCart.user_id == current_user.id)

def get_favorite_query(id, current_user):
    return select(Favorite).where(Favorite.recipe_id == id, Favorite.user_id == current_user.id)
####### сделать красиво как в коде ниже
def get_result_favorite(user_id: int, recipe_ids: list[int]):
    return select(Favorite.recipe_id).where(
        Favorite.user_id == user_id).where(
        Favorite.recipe_id.in_(recipe_ids)
    )

def get_result_cart(user_id: int, recipe_ids: list[int]):
    return select(ShoppingCart.recipe_id).where(
        ShoppingCart.user_id == user_id).where(
            ShoppingCart.recipe_id.in_(recipe_ids)
        )


async def get_user_recipe_flags(
        session: AsyncSession, 
        user_id: int,
        recipe_ids: list[int]
    ):
    if not recipe_ids:
        return set(), set()
    favorite_stmt = select(Favorite.recipe_id).where(
    Favorite.user_id == user_id,
    Favorite.recipe_id.in_(recipe_ids)
    )
    
    cart_stmt = select(ShoppingCart.recipe_id).where(
    ShoppingCart.user_id == user_id,
    ShoppingCart.recipe_id.in_(recipe_ids)
    )
    favorite_ids = set((await session.execute(favorite_stmt)).scalars().all())
    cart_ids = set((await session.execute(cart_stmt)).scalars().all())
    return favorite_ids, cart_ids