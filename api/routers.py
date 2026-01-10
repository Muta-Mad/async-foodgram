from fastapi import APIRouter

from api.users.auth.views import router as auth_router
from api.users.views import router as users_router
from api.recipes.views import router as recipe_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(recipe_router)