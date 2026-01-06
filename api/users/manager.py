import logging

from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin

from api.core.settings import settings
from api.users.auth.get_db import get_user_db
from api.users.models import User

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Менеджер для работы с пользователем"""
    verification_token_secret = settings.access_token.verification_token_secret
    reset_password_token_secret = settings.access_token.reset_password_token_secret


async def get_user_manager(user_db=Depends(get_user_db)):
    """Получить менеджер"""
    yield UserManager(user_db)
