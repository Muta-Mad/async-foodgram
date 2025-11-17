from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy import Enum
import enum


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), unique=True)
    last_name: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)


class Tag(Base):
    """ Модель Тега """

    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    slug: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        comment="Поле для слэга",
        )


class MeasurementUnit(enum.Enum):
    """ Класс, представляющий константы единицы измерения. """

    GRAM = "г", "Грамм"
    KILOGRAM = "кг", "Килограмм"
    LITER = "л", "Литр"
    MILLILITER = "мл", "Миллилитр"
    PIECE = "шт", "Штука"


class Ingredient(Base):
    """ Модель Ингредиента """

    __tablename__ = 'ingredients'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    measurement_unit: Mapped[MeasurementUnit] = mapped_column(
        Enum(MeasurementUnit, name='measurement_unit_enum'),
    )
