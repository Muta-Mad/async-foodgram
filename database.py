from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from settings import settings


database_url = settings.db.url

engine = create_async_engine(database_url)

new_session = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=False, class_=AsyncSession
)


async def get_db():
    """асинхронная функция для получении сессии"""
    async with new_session() as session:
        try:
            yield session
        finally:
            await session.close()
