from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text

from api.models import Base

class User(SQLAlchemyBaseUserTable[int], Base,):
    __tablename__ = "user"  
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    avatar: Mapped[str] = mapped_column(Text)