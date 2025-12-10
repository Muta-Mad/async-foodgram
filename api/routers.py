from fastapi import APIRouter

from api.tags.tags import router as tag_router
from api.ingredients.ingredients import router as ingredient_router
from api.users.routers import router as auth_router
from api.users.users import router as users_router
from api.example.tags import router as example_router

router = APIRouter()
router.include_router(tag_router)
router.include_router(ingredient_router)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(example_router)
