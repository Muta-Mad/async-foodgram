import enum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class MeasurementUnit(enum.Enum):
    """ Класс, представляющий константы единицы измерения. """

    GRAM = "г", "Грамм"
    KILOGRAM = "кг", "Килограмм"
    LITER = "л", "Литр"
    MILLILITER = "мл", "Миллилитр"
    PIECE = "шт", "Штука"


class Ingredient(Base):
    __tablename__ = 'ingredients'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    measurement_unit: Mapped[MeasurementUnit] = mapped_column(
        Enum(MeasurementUnit, name='measurement_unit_enum'),
    )
