
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_users.exceptions import UserAlreadyExists
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.fastapiusers import fastapi_users
from api.users.models import User
from api.users.schemas import UserRead, UserUpdate, UserCreate, UserResponse
from database import get_db


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
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь уже существует'
        )
    
@router.get('/', response_model=list[UserResponse])
async def get_all_users(
    session: AsyncSession = Depends(get_db)
):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users 