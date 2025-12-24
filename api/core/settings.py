from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent

DB_PATH = BASE_DIR / 'db.sqlite3'


class Db_Config(BaseModel):
    """Настройки базы данных"""
    url: str = f'sqlite+aiosqlite:///{DB_PATH}'


class Paginate_Config(BaseModel):
    page_size: int = 6


class Access_Token(BaseModel):
    """Настройки токена"""
    lifetime_seconds: int = 3600
    verification_token_secret: str
    reset_password_token_secret: str

class Settings(BaseSettings):
    """Базовые настройки"""
    db: Db_Config = Db_Config()
    access_token: Access_Token
    pagination: Paginate_Config = Paginate_Config()

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_nested_delimiter='__',
    )

settings = Settings()# type: ignore
