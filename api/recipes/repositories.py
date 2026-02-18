from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.cart.models import ShoppingCart
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
        is_favorited=recipe.id in favorites_set,
        is_in_shopping_cart=recipe.id in cart_set,
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

def recipe_relations():
    return (
        selectinload(Recipe.author),
        selectinload(Recipe.tags),
        selectinload(Recipe.ingredients),
    )

def get_recipes_query():
    return (
        select(Recipe)
        .options(
            *recipe_relations()
        )
        .order_by(Recipe.id)
    )

def get_recipe_query(id: int):
    return (
        select(Recipe)
        .options(
            *recipe_relations()
        )
        .where(Recipe.id==id)
    )

async def get_owned_recipe(
    session: AsyncSession,
    recipe_id: int,
    user_id: int,
) -> Recipe:
    query = (
    select(Recipe)
    .options(
        *recipe_relations()
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

def map_user_to_read(user: User) -> UserRead:
    return UserRead.model_validate(user)

def map_tag_to_read(tag: Tag) -> TagRead:
    return TagRead.model_validate(tag)

def map_ingredient_to_read(ingredient: Ingredient) -> IngredientRead:
    return IngredientRead.model_validate(ingredient)


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


def get_tags_query():
    return select(Tag).order_by(Tag.id)

def get_tag_query(id):
    return select(Tag).where(Tag.id == id)

def get_ingredients_query():
    return select(Ingredient).order_by(Ingredient.id)

def get_ingredient_query(id):
    return select(Ingredient).where(Ingredient.id == id)


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
    favorite_stmt = get_result_favorite(user_id, recipe_ids)
    cart_stmt = get_result_cart(user_id, recipe_ids)

    favorite_ids = set((await session.execute(favorite_stmt)).scalars().all())
    cart_ids = set((await session.execute(cart_stmt)).scalars().all())
    return favorite_ids, cart_ids

async def get_full_recipe(
    session: AsyncSession,
    recipe_id: int
) -> Recipe:
    stmt = get_recipe_query(recipe_id)
    result = await session.execute(stmt)
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise GlobalError.not_found('Рецепт не найден.')
    return recipe
