from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schemas.user import UserCreate, UserRead
from services.user_service import UserService

router = APIRouter(prefix='/users', tags=['Users'])

user_service = UserService()


@router.get('/', response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(get_db)):
    users = await user_service.get_all_users(session=session)
    return users


@router.post('/', response_model=UserRead)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    user = await user_service.create_user(
        session=session,
        user_create=user_data
    )
    return user
