from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent

DB_PATH = BASE_DIR / 'db.sqlite3'


class Db_Config(BaseModel):
    url: str = f'sqlite+aiosqlite:///{DB_PATH}'



class Settings(BaseSettings):
    db: Db_Config = Db_Config()
    api_prefix: str = '/api'


settings = Settings()