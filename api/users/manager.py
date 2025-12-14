import logging

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from api.users.auth.get_db import get_user_db
from api.users.models import User
from settings import settings

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    verification_token_secret = settings.access_token.verification_token_secret
    reset_password_token_secret = settings.access_token.reset_password_token_secret

    async def on_after_register(
            self, 
            user: User, 
            request: Request | None = None
    ):
        log.warning('Пользователь %r зарегистрирован.', user.id)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
