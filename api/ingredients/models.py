from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from api.basemodel import Base
from api.mixins import SQLAlchemyBaseMixin


class Ingredient(Base, SQLAlchemyBaseMixin):
    """Модель Ингредиента"""

    __tablename__ = 'ingredients'
    measurement_unit: Mapped[str] = mapped_column(String(20))
