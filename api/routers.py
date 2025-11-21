from fastapi import APIRouter

from api.tags.routers import router as tags_router

router = APIRouter()
router.include_router(tags_router)