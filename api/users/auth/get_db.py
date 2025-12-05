from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from api.users.models import User, AccessToken
from database import get_db 

async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield User.get_db(session=session)


async def get_access_token_db(
    session: AsyncSession = Depends(get_db),
):  
    yield AccessToken.get_db(session=session)