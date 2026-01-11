from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.base_paginator import Paginator
from api.core.exceptions import GlobalError
from api.core.paginate_schemas import Page
from api.recipes.models import Recipe
from api.recipes.repositories import get_amount_map, get_recipes_query, map_recipe_to_read, get_recipe_query
from api.recipes.schemas import RecipeRead
from api.core.database import get_db


router = APIRouter(prefix='/recipes', tags=['Recipes'])


@router.get('/', response_model=Page[RecipeRead])
async def get_recipes(
    paginator: Paginator = Depends(),
    session: AsyncSession = Depends(get_db),
):
    query = get_recipes_query()
    paginated_data = await paginator.get_paginate(
        session=session,
        model=Recipe,
        base_query=query
    )
    recipes = paginated_data['results']
    recipe_ids = [recipe.id for recipe in recipes]
    amount_map = await get_amount_map(session, recipe_ids)
    recipes_out = [
        map_recipe_to_read(recipe, amount_map)

        for recipe in recipes
    ]

    return Page(
        count=paginated_data['count'],
        next=paginated_data['next'],
        previous=paginated_data['previous'],
        results=recipes_out
    )

@router.get('/{id}', response_model=RecipeRead)
async def get_recipe(
    id: int,
    session: AsyncSession = Depends(get_db),
) -> RecipeRead: 
    query = get_recipe_query(id)
    result = await session.execute(query)
    recipe = result.scalar_one_or_none()
    if not recipe:
        GlobalError.not_found('Рецепт с таким id не найден')
    recipe_id = [recipe.id]
    amount_map = await get_amount_map(session, recipe_id)
    recipes_out = map_recipe_to_read(recipe, amount_map)
    return recipes_out