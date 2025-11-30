from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SQLAlchemyBaseMixin:
    """
    Миксин, содержащий поле идентификатора
    и названия для моделей ингредиент и тег.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
