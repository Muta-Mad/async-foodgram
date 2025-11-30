from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase, 
    SQLAlchemyBaseAccessTokenTable,
)

from api.basemodel import Base

class User(SQLAlchemyBaseUserTable[int], Base,):
    """Модель пользователя"""
    __tablename__ = 'users'  
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    avatar: Mapped[str] = mapped_column(Text)

    @classmethod
    def get_db(cls, session: AsyncSession):
        """Возвращает объект работы с пользователями через FastAPI-Users."""
        return SQLAlchemyUserDatabase(session, cls)


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[int]):
    """модель токена доступа пользователя."""
    __tablename__ = 'access_tokens'  
    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('users.id', ondelete='cascade'), 
        nullable=False
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        """Возвращает объект работы с токенами доступа."""
        return SQLAlchemyAccessTokenDatabase(session, cls)