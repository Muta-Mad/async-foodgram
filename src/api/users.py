import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from schemas.user import UserCreate, UserRead
from services.user_service import UserService


logger = logging.getLogger(__name__)

router = APIRouter(prefix='/users', tags=['Users'])


def get_user_service() -> UserService:
    return UserService()


@router.get('/', response_model=list[UserRead])
async def get_users(
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    try:
        users = await user_service.get_all(session=session)
        return users
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Критическая ошибка в get_users",
            exc_info=True,
            extra={
                "endpoint": "GET /users",
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка."
        )


@router.post('/', response_model=UserRead)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    try:
        user = await user_service.create(
            session=session,
            obj_in=user_data
        )
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Критическая ошибка в create_user",
            exc_info=True,
            extra={
                "endpoint": "POST /users",
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка."
        )
