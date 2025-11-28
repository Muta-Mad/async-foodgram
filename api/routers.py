from fastapi import APIRouter

from .tags.routers import tags_router
from .ingredients.routers import ingredient_router

router = APIRouter()
router.include_router(tags_router)
router.include_router(ingredient_router)
