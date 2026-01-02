from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_db
from api.core.exceptions import GlobalError
from api.ingredients.models import Ingredient
from api.ingredients.schemas import IngredientRead

router = APIRouter(prefix='/ingredients', tags=['Ingredients'])


async def get_all_ingredients(session: AsyncSession) -> list[Ingredient]:
    """Логика, возвращающая список ингредиентов"""
    stmt = select(Ingredient).order_by(Ingredient.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_ingredient_object(
    session: AsyncSession,
    id: int,
) -> Ingredient|None:
    """Логика, возвращающая объект ингредиента по id"""
    stmt = select(Ingredient).where(Ingredient.id == id)
    result = await session.scalar(stmt)
    if not result:
        GlobalError.not_found('Ингредиент')
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
) -> Ingredient|None:
    """get - запрос для получения объекта ингредиента по id"""
    ingredient = await get_ingredient_object(session, id)
    return ingredient
