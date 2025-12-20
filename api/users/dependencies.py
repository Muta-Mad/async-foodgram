from fastapi import Depends, HTTPException, Request, status
from fastapi_users.authentication.strategy import Strategy

from api.users.auth.strategies import get_database_strategy
from api.users.auth.transport import token_transport
from api.users.manager import UserManager, get_user_manager
from api.users.models import User


async def get_current_user(
    request: Request,
    token: str = Depends(token_transport),
    strategy: Strategy = Depends(get_database_strategy),
    user_manager: UserManager = Depends(get_user_manager)
) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    user = await strategy.read_token(token, user_manager)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return user