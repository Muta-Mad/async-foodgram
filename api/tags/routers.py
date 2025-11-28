from fastapi import APIRouter

from .tags import router

tags_router = APIRouter()
tags_router.include_router(router)
