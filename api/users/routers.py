from fastapi import APIRouter

from api.users.auth.backend import authentication_backend
from api.users.fastapiusers import fastapi_users

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
