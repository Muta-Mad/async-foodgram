from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (SQLAlchemyAccessTokenDatabase,
                                                      SQLAlchemyBaseAccessTokenTable)
from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.core.basemodel import Base
from api.core.idmixin import IdPkMixin


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

    subscriptions: Mapped[list['Follow']] = relationship(
        'Follow', 
        foreign_keys='Follow.follower_id', 
        back_populates='follower',
        cascade='all, delete-orphan'
    )
    subscribers: Mapped[list['Follow']] = relationship(
        'Follow', 
        foreign_keys='Follow.author_id', 
        back_populates='author',
        cascade='all, delete-orphan'
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        """Возвращает объект работы с пользователями через FastAPI-Users."""
        return SQLAlchemyUserDatabase(session, cls)


class AccessToken(
    Base, 
    SQLAlchemyBaseAccessTokenTable[int]
):
    """модель токена доступа пользователя."""

    __tablename__ = 'auth_tokens'
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='cascade'), nullable=False
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        """Возвращает объект работы с токенами доступа."""
        return SQLAlchemyAccessTokenDatabase(session, cls)


class Follow(Base, IdPkMixin):
    __tablename__ = 'subscribes'
    __table_args__ = (
        UniqueConstraint('follower_id', 'author_id', name='uniq_follow'),
    )
    follower_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='cascade'))
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='cascade'))

    follower: Mapped['User'] = relationship(
        foreign_keys=[follower_id],
        back_populates='subscriptions')
    
    author: Mapped['User'] = relationship(
        foreign_keys=[author_id],
        back_populates='subscribers'
    )