from fastapi import APIRouter

from .views import router as users_router
from .tags import router as tags_router
from .ingredients import router as ingredient_router

router = APIRouter()
router.include_router(users_router)
router.include_router(tags_router)
router.include_router(ingredient_router)