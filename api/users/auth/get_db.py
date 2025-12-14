from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.models import AccessToken, User
from database import get_db


def create_db_dependency(model_class):
    async def dependency(session: AsyncSession = Depends(get_db)):
        yield model_class.get_db(session=session)
    return dependency


get_user_db = create_db_dependency(User)
get_access_token_db = create_db_dependency(AccessToken)