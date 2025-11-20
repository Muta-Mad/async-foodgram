from fastapi import APIRouter

from api.users import router as users_router
from api.tags import router as tags_router
from api.ingredients import router as ingredient_router

router = APIRouter()
router.include_router(users_router)
router.include_router(tags_router)
router.include_router(ingredient_router)
