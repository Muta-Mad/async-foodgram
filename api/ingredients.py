from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import get_db
from .models import Ingredient
from .schemas import IngredientRead

router = APIRouter(prefix='/ingredients', tags=['Ingredients'])


async def get_ingredient_object(session: AsyncSession, id: int):
    """ Логика для получения объекта ингредиента """
    stmt = select(Ingredient).where(Ingredient.id == id)
    result = await session.scalar(stmt)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такого ингредиента не существует.'
        )
    return result


async def get_all_ingredients(session: AsyncSession):
    """ Логика для получения списка ингредиентов. """
    stmt = select(Ingredient).order_by(Ingredient.id)
    result = await session.scalars(stmt)
    return result.all()


@router.get('/', response_model=list[IngredientRead])
async def get_ingredients(session: AsyncSession = Depends(get_db)):
    """ Асинхронный роутер для получения списка ингредиентов """
    return await get_all_ingredients(session)


@router.get('/{id}', response_model=IngredientRead)
async def get_ingredient(id: int, session: AsyncSession = Depends(get_db)):
    """ Асинхронный роутер для получения объекта ингредиента по id """
    ingredient = await get_ingredient_object(session, id)
    return ingredient
