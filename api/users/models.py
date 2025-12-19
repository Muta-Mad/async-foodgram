from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (SQLAlchemyAccessTokenDatabase,
                                                      SQLAlchemyBaseAccessTokenTable)
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from api.basemodel import Base
from api.idmixin import IdPkMixin


class User(
    Base,
    IdPkMixin,
    SQLAlchemyBaseUserTable[int],
):
    """Модель пользователя"""
    __tablename__ = 'users'
    first_name: Mapped[str] = mapped_column(String(length=150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(length=150), nullable=False)
    username: Mapped[str] = mapped_column(String(length=150), unique=True, nullable=False)
    avatar: Mapped[str | None]


    @classmethod
    def get_db(cls, session: AsyncSession):
        """Возвращает объект работы с пользователями через FastAPI-Users."""
        return SQLAlchemyUserDatabase(session, cls)

class AccessToken(
    Base, 
    SQLAlchemyBaseAccessTokenTable[int]
):
    """модель токена доступа пользователя."""

    __tablename__ = 'auth_token'
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='cascade'), nullable=False
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        """Возвращает объект работы с токенами доступа."""
        return SQLAlchemyAccessTokenDatabase(session, cls)
