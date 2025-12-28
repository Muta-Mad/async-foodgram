from fastapi import APIRouter

from api.ingredients.ingredients import router as ingredient_router
from api.tags.tags import router as tag_router
from api.users.auth.views import router as auth_router
from api.users.views import router as users_router

router = APIRouter()
router.include_router(tag_router)
router.include_router(ingredient_router)
router.include_router(auth_router)
router.include_router(users_router)