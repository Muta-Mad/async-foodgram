
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_users.exceptions import UserAlreadyExists
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import not_found_error
from api.users.fastapiusers import fastapi_users
from api.users.models import User
from api.users.schemas import UserCreate, UserRead, UserResponce
from database import get_db


router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', response_model=UserResponce, status_code=201)
async def create_user(
    user_create: UserCreate,
    user_manager=Depends(fastapi_users.get_user_manager),
    session: AsyncSession = Depends(get_db)
)-> User | None:
    result = await session.execute(select(User).where(User.username == user_create.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким username уже существует'
        )
    try:
        user = await user_manager.create(user_create, safe=True)
        return user
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь уже существует'
        )
    
@router.get('/', response_model=list[UserRead])
async def users(
    session: AsyncSession = Depends(get_db)
)-> list[User]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return list(users) 

@router.get('/me', response_model=UserRead)
async def me(
    user=Depends(fastapi_users.current_user(active=True))
)-> User:
    return user


@router.get('/{id}', response_model=UserRead)
async def user(
    id: int,
    session: AsyncSession = Depends(get_db)
)-> User | None:
    result = await session.execute(
        select(User).where(User.id == id)
    )
    user = result.scalar_one_or_none()
    if not user:
        not_found_error('Страница не найдена.')
    return user
