from fastapi import APIRouter

from api.users.fastapiusers import fastapi_users
from api.users.schemas import UserRead, UserUpdate


router = APIRouter(prefix='/users', tags=['Users'])

# /users
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)