from fastapi import APIRouter

from api.users.fastapiusers import fastapi_users
from api.users.schemas import UserRead, UserUpdate, UserCreate


router = APIRouter(prefix='/users', tags=['Users'])

# /users
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate)
)
