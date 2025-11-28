from fastapi import APIRouter

from .ingredients import router

ingredient_router = APIRouter()
ingredient_router.include_router(router)
