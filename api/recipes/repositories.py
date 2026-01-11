from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.recipes.models import Recipe, RecipeIngredient, Tag
from api.recipes.schemas import IngredientInRecipe, RecipeRead, TagRead
from api.users.models import User
from api.users.schemas import UserRead


def map_recipe_to_read(
    recipe: Recipe,
    amount_map: dict[tuple[int, int], int],
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
        .order_by(Recipe.id).where(Recipe.id==id)
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
