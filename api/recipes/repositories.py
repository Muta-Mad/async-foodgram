from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
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
    favorites_set: set[int],
    cart_set: set[int]
) -> RecipeRead:
    ingredients = [
        IngredientInRecipe(
            id=ri.ingredient.id,
            name=ri.ingredient.name,
            measurement_unit=ri.ingredient.measurement_unit,
            amount=ri.amount,
        )
        for ri in recipe.recipe_ingredients
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


def recipe_relations():
    return (
        selectinload(Recipe.author),
        selectinload(Recipe.tags),
        selectinload(Recipe.recipe_ingredients).selectinload(RecipeIngredient.ingredient),
    )

def get_recipes_query(
    current_user: User | None = None,
    is_favorited: bool | None = None,
    is_in_shopping_cart: bool | None = None,
    author: int | None = None,
    tags: list[str] | None = None,
):
    query = select(Recipe).options(*recipe_relations())
    if author:
        query = query.where(Recipe.author_id == author)
    if tags:
        query = query.join(Recipe.tags).where(Tag.slug.in_(tags))

    if is_favorited and current_user:
        query = query.join(Favorite).where(
            Favorite.user_id == current_user.id
        )
    if is_in_shopping_cart and current_user:
        query = query.join(ShoppingCart).where(
            ShoppingCart.user_id == current_user.id
        )
    return query.order_by(Recipe.id).distinct()

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

async def set_recipe_ingredients(
    session: AsyncSession,
    recipe: Recipe,
    ingredients: list,
):
    await session.execute(
        delete(RecipeIngredient).where(
            RecipeIngredient.recipe_id == recipe.id
        )
    )

    new_items = [
        RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=item.id,
            amount=item.amount,
        )
        for item in ingredients
    ]

    session.add_all(new_items)

async def set_recipe_tags(
    session: AsyncSession,
    recipe: Recipe,
    tags: list[int],
    ):
    await session.execute(delete(RecipeTag).where(RecipeTag.recipe_id == recipe.id))

    new_items = [
        RecipeTag(
            recipe_id=recipe.id,
            tag_id=tag_id
        )
        for tag_id in tags
    ]
    session.add_all(new_items)

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
    stmt = (
        select(Recipe)
        .options(
            selectinload(Recipe.author),
            selectinload(Recipe.tags),
            selectinload(Recipe.recipe_ingredients)
                .selectinload(RecipeIngredient.ingredient),
        )
        .where(Recipe.id == recipe_id)
    )
    result = await session.execute(stmt)
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise GlobalError.not_found('Рецепт не найден.')
    return recipe

async def validate_ingredients(
    session: AsyncSession,
    ingredient_data: list
):
    ingredien_ids = [item.id for item in ingredient_data]
    ingredien_ids_set = set(ingredien_ids)

    result = await session.execute(
        select(Ingredient.id).where(
            Ingredient.id.in_(ingredien_ids_set))
        )
    existing_ids = set(result.scalars().all())
    if ingredien_ids_set != existing_ids:
        GlobalError.bad_request('Нет такого ингредиента!')
    if len(ingredien_ids) != len(ingredien_ids_set):
        GlobalError.bad_request('Ингредиенты не должны повторяться')

async def validate_tags(
    session: AsyncSession,
    tag_ids: list
):
    tag_ids_set = set(tag_ids)
    result = await session.execute(
        select(Tag.id).where(
            Tag.id.in_(tag_ids_set))
        )
    existing_ids = set(result.scalars().all())
    if tag_ids_set != existing_ids:
        GlobalError.bad_request('Нет такого тега')
    if len(tag_ids) != len(tag_ids_set):
        GlobalError.bad_request('Теги не должны повторяться')

