from fastapi import APIRouter

from api.users.fastapiusers import fastapi_users
from api.users.auth.backend import authentication_backend
from api.users.schemas import UserRead, UserCreate


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

# /login
# /logout
router.include_router(
    fastapi_users.get_auth_router(
        authentication_backend), prefix='/token'
)

# /register
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
