from fastapi import Depends
from fastapi_users.authentication.strategy.db import (AccessTokenDatabase,
                                                      DatabaseStrategy)

from api.core.settings import settings
from api.users.auth.get_db import get_access_token_db
from api.users.models import AccessToken


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=settings.access_token.lifetime_seconds)