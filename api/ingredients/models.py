from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from api.basemodel import Base


class Ingredient(Base):
    """Модель Ингредиента"""

    __tablename__ = 'ingredients'
    name: Mapped[str] = mapped_column(String(128))
    measurement_unit: Mapped[str] = mapped_column(String(20))
