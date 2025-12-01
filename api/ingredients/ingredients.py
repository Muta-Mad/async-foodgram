from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from database import get_db
from api.ingredients.models import Ingredient
from api.ingredients.schemas import IngredientRead
from api.exceptions import not_found_error

router = APIRouter(prefix='/ingredients', tags=['Ingredients'])


async def get_all_ingredients(session: AsyncSession) -> list[Ingredient]:
    """Логика, возвращающая список ингредиентов"""
    stmt = select(Ingredient).order_by(Ingredient.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_ingredient_object(
    session: AsyncSession,
    id: int,
) -> Optional[Ingredient]:
    """Логика, возвращающая объект ингредиента по id"""
    stmt = select(Ingredient).where(Ingredient.id == id)
    result = await session.scalar(stmt)
    if not result:
        not_found_error('Ингредиент')
    return result


@router.get('/', response_model=list[IngredientRead])
async def get_ingredients(
    session: AsyncSession = Depends(get_db),
) -> list[Ingredient]:
    """get - запрос для получения списка ингредиентов"""
    ingredient = await get_all_ingredients(session)
    return ingredient


@router.get('/{id}', response_model=IngredientRead)
async def get_ingredient(
    id: int,
    session: AsyncSession = Depends(get_db),
) -> Optional[Ingredient]:
    """get - запрос для получения объекта ингредиента по id"""
    ingredient = await get_ingredient_object(session, id)
    return ingredient
