from fastapi import APIRouter

from api.tags.tags import router as tag_router
from api.ingredients.ingredients import router as ingredient_router

router = APIRouter()
router.include_router(tag_router)
router.include_router(ingredient_router)
