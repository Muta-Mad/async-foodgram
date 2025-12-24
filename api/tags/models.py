from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from api.core.basemodel import Base
from api.core.idmixin import IdPkMixin


class Tag(IdPkMixin, Base):
    """Модель Тега"""

    __tablename__ = 'tags'
    name: Mapped[str] = mapped_column(String(32))
    slug: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        comment='Поле для слэга',
    )
