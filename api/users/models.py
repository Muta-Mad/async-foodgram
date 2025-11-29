from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text

from api.basemodel import Base

class User(SQLAlchemyBaseUserTable[int], Base,):
    __tablename__ = 'users'  
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    avatar: Mapped[str] = mapped_column(Text)