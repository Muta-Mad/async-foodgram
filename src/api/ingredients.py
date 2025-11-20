import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schemas.ingredient import IngredientCreate, IngredientRead
from services.ingredient_service import IngredientService


logger = logging.getLogger(__name__)

router = APIRouter(prefix='/ingredients', tags=['Ingredients'])


def get_ingredient_service() -> IngredientService:
    return IngredientService()


@router.get('/', response_model=list[IngredientRead])
async def get_ingredients(
    session: AsyncSession = Depends(get_db),
    ingredient_service: IngredientService = Depends(get_ingredient_service)
):
    try:
        ingredients = await ingredient_service.get_all(session=session)
        return ingredients
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Критическая ошибка в get_ingredients",
            exc_info=True,
            extra={
                "endpoint": "GET /ingredients",
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка."
        )


@router.post('/', response_model=IngredientRead)
async def create_ingredient(
    ingredient_data: IngredientCreate,
    session: AsyncSession = Depends(get_db),
    ingredient_service: IngredientService = Depends(get_ingredient_service)
):
    try:
        user = await ingredient_service.create(
            session=session,
            obj_in=ingredient_data
        )
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Критическая ошибка в create_ingredient",
            exc_info=True,
            extra={
                "endpoint": "POST /ingredients",
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка."
        )
