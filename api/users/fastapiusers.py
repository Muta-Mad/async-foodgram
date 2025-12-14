
from fastapi_users import FastAPIUsers

from api.users.auth.backend import authentication_backend
from api.users.manager import get_user_manager
from api.users.models import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)
