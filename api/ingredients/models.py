import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy import Enum

from api.basemodel import Base


class MeasurementUnit(enum.Enum):
    """Класс, представляющий константы единицы измерения"""

    GRAM = 'г'
    KILOGRAM = 'кг'
    LITER = 'л'
    MILLILITER = 'мл'
    PIECE = 'шт'


class Ingredient(Base):
    '''Модель Ингредиента'''

    __tablename__ = 'ingredients'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    measurement_unit: Mapped[MeasurementUnit] = mapped_column(
        Enum(MeasurementUnit, name='measurement_unit_enum'),
    )
