from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from api.basemodel import Base, SQLAlchemyBaseMixin


class Tag(Base, SQLAlchemyBaseMixin):
    """Модель Тега"""

    __tablename__ = 'tags'
    slug: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        comment='Поле для слэга',
    )
