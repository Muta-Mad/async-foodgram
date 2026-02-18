from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.base_paginator import Paginator
from api.core.exceptions import GlobalError
from api.core.paginate_schemas import Page
from api.dependencies import get_current_user, get_current_user_optional
from api.recipes.models import Recipe, RecipeIngredient, RecipeTag
from api.recipes.repositories import (
    get_amount_map, get_full_recipe, get_owned_recipe, 
    get_recipes_query, get_user_recipe_flags, map_recipe_to_read, get_recipe_query,
    set_recipe_ingredients, set_recipe_tags
)
from api.recipes.schemas import RecipeCreate, RecipeRead, RecipeUpdate
from api.core.database import get_db
from api.users.models import User


router = APIRouter(prefix='/recipes', tags=['Recipes'])

@router.get('/', response_model=Page[RecipeRead])
async def get_recipes(
    paginator: Paginator = Depends(),
    session: AsyncSession = Depends(get_db),
    current_user: User  = Depends(get_current_user_optional),
):
    query = get_recipes_query()
    paginated_data = await paginator.get_paginate(
        session=session,
        model=Recipe,
        base_query=query
    )
    recipes = paginated_data['results']
    recipe_ids = [recipe.id for recipe in recipes]
    favorites_set = set()
    cart_set = set()
    if current_user and recipe_ids:
        favorites_set, cart_set = await get_user_recipe_flags(
            session=session, user_id=current_user.id, recipe_ids=recipe_ids
        )
    amount_map = await get_amount_map(session, recipe_ids)
    recipes_out = [
        map_recipe_to_read(recipe, amount_map, favorites_set, cart_set)
        for recipe in recipes
    ]
    return Page(
        count=paginated_data['count'],
        next=paginated_data['next'],
        previous=paginated_data['previous'],
        results=recipes_out
    )

@router.get('/{id}/', response_model=RecipeRead)
async def get_recipe(
    id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User  = Depends(get_current_user_optional),
) -> RecipeRead: 
    query = get_recipe_query(id)
    result = await session.execute(query)
    recipe = result.scalar_one_or_none()
    if not recipe:
        GlobalError.not_found('Рецепт с таким id не найден')
    favorites_set = set()
    cart_set = set()
    if current_user:
        favorites_set, cart_set = await get_user_recipe_flags(
            session=session, user_id=current_user.id, recipe_ids=[recipe.id]
        )
    amount_map = await get_amount_map(session, [recipe.id])
    return map_recipe_to_read(recipe, amount_map, favorites_set, cart_set)

@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = await get_owned_recipe(session, id, current_user.id)
    await session.delete(recipe)
    await session.commit()

@router.post('/', response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
async def recipe_create(
    data: RecipeCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    recipe = Recipe(
        author_id=current_user.id, 
        name=data.name, 
        image=data.image, 
        text=data.text, 
        cooking_time=data.cooking_time
    )
    session.add(recipe)
    await session.flush()
    recipe_ingredients = [
        RecipeIngredient(
            recipe_id=recipe.id, 
            ingredient_id=item.id, 
            amount=item.amount
            ) 
            for item in data.ingredients
        ]
    session.add_all(recipe_ingredients)
    tags = [
        RecipeTag(
            recipe_id=recipe.id, 
            tag_id=tag) 
            for tag in data.tags
        ]
    session.add_all(tags)
    await session.commit()
    recipe_to_read = await get_full_recipe(session=session, recipe_id=recipe.id)
    amount_map = await get_amount_map(session, [recipe.id])
    return map_recipe_to_read(recipe_to_read, amount_map, set(), set(),)

@router.patch('/{id}/', response_model=RecipeRead)
async def recipe_update(
    id: int,
    new_data: RecipeUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = await get_owned_recipe(session, id, current_user.id)
    if new_data.name is not None:
        recipe.name = new_data.name
    if new_data.text is not None:
        recipe.text = new_data.text
    if new_data.image is not None:
        recipe.image = new_data.image
    if new_data.cooking_time is not None:
        recipe.cooking_time = new_data.cooking_time
    if new_data.ingredients is not None:
        set_recipe_ingredients(recipe, new_data.ingredients)
    if new_data.tags is not None:
        set_recipe_tags(recipe, new_data.tags)
    await session.commit()
    favorites_set, cart_set = await get_user_recipe_flags(
        session=session, 
        user_id=current_user.id, 
        recipe_ids=[recipe.id]
    )
    recipe_to_read = await get_full_recipe(session=session, recipe_id=recipe.id)
    amount_map = await get_amount_map(session, [recipe.id])
    return map_recipe_to_read(recipe_to_read, amount_map, favorites_set=favorites_set,cart_set=cart_set)

