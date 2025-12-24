from fastapi import Depends, HTTPException, Request, status
from fastapi_users.authentication.strategy import Strategy
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.baserepository import BaseRepository
from api.core.database import get_db
from api.core.exceptions import Exception
from api.users.auth.get_db import get_user_db
from api.users.auth.strategies import get_database_strategy
from api.users.auth.transport import token_transport
from api.users.manager import UserManager, get_user_manager
from api.users.models import User


async def get_user_manager(user_db=Depends(get_user_db)):
    """создает зависимость для работы с пользователями"""
    yield UserManager(user_db)


async def get_current_user(
    request: Request,
    token: str = Depends(token_transport),
    strategy: Strategy = Depends(get_database_strategy),
    user_manager: UserManager = Depends(get_user_manager)
) -> User | None:
    """достает текущего пользователя."""
    if not token:
        Exception.unauthorized()
    user = await strategy.read_token(token, user_manager)
    if not user:
        Exception.unauthorized()
    return user

async def get_repository(
        session: AsyncSession = Depends(get_db)
    ):
    """создает зависимость для BaseRepository"""
    return BaseRepository(session)