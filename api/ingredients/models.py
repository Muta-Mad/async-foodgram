from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from api.basemodel import Base
from api.idmixin import IdPkMixin

class Ingredient(IdPkMixin, Base):
    """Модель Ингредиента"""

    __tablename__ = 'ingredients'
    name: Mapped[str] = mapped_column(String(128))
    measurement_unit: Mapped[str] = mapped_column(String(20))
