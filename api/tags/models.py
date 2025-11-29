from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from api.basemodel import Base


class Tag(Base):
    __tablename__ = 'tags'
    name: Mapped[str] = mapped_column(String(128))
    slug: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        comment='Поле для слэга',
        )
    