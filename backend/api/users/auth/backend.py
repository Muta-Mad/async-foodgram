from fastapi_users.authentication import AuthenticationBackend

from api.users.auth.strategies import get_database_strategy
from api.users.auth.transport import token_transport

authentication_backend = AuthenticationBackend(
    name='auth_token',
    transport=token_transport,
    get_strategy=get_database_strategy,
)
