from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from api.core.basemodel import Base
from api.core.idmixin import IdPkMixin


class Ingredient(IdPkMixin, Base):
    """Модель Ингредиента"""

    __tablename__ = 'ingredients'
    name: Mapped[str] = mapped_column(String(128))
    measurement_unit: Mapped[str] = mapped_column(String(20))
