
from fastapi_users import FastAPIUsers

from api.users.models import User
from api.users.manager import get_user_manager
from api.users.auth.backend import authentication_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)
