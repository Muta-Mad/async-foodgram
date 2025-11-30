from fastapi import APIRouter

from api.tags.routers import tags_router
from api.ingredients.routers import ingredient_router

router = APIRouter()
router.include_router(tags_router)
router.include_router(ingredient_router)
