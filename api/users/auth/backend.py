from fastapi_users.authentication import AuthenticationBackend

from api.users.auth.transport import bearer_transport
from api.users.auth.strategies import get_database_strategy

authentication_backend = AuthenticationBackend(
    name='auth_token',
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
