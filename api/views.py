from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserRead, UserCreate
from .database import get_db

router = APIRouter(prefix='/users', tags=['Users'])


async def get_all_users(session: AsyncSession):
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def post_create_user(session: AsyncSession, user_create: UserCreate,) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get('/', response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(get_db)):
    users = await get_all_users(session=session)
    return users

@router.post('/', response_model=UserRead)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    user = await post_create_user(session=session, user_create=user_data)
    return user