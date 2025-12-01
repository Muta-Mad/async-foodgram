from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from api.basemodel import Base


class Ingredient(Base):
    """Модель Ингредиента"""

    __tablename__ = 'ingredients'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    measurement_unit: Mapped[str] = mapped_column(String(20))
