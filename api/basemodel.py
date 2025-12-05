from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Абстрактная модель, наследник DeclarativeBase """
    __abstract__ = True

    