from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

from api.constants import (MAX_LENGTH_FIRST_NAME, 
                               MAX_LENGTH_LAST_NAME, 
                               MAX_LENGTH_EMAIL
                               )


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(MAX_LENGTH_FIRST_NAME), unique=True)
    last_name: Mapped[str] = mapped_column(String(MAX_LENGTH_LAST_NAME), unique=True)
    email: Mapped[str] = mapped_column(String(MAX_LENGTH_EMAIL), unique=True)