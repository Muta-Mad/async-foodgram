from fastapi import APIRouter, Depends, HTTPException, status

from api.users.fastapiusers import fastapi_users
from api.users.schemas import UserRead, UserUpdate, UserCreate, UserResponse


router = APIRouter(prefix='/users', tags=['Users'])

# /users
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)

@router.post('/', response_model=UserResponse, status_code=201)
async def create_user(
    user_create: UserCreate,
    user_manager=Depends(fastapi_users.get_user_manager)
):
    try:
        user = await user_manager.create(user_create, safe=True)
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))