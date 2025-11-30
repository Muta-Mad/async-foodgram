from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class SQLAlchemyBaseMixin:
    """
    Миксин, содержащий поле идентификатора
    и названия для моделей ингредиент и тег.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
