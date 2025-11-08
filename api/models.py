from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), unique=True)
    last_name: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)