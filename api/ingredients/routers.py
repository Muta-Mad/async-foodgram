from fastapi import APIRouter

from api.ingredients.ingredients import router

ingredient_router = APIRouter()
ingredient_router.include_router(router)
