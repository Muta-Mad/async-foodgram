import sys
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.api.models import Base


engine = create_async_engine('sqlite+aiosqlite:///./sqlite.db')

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with new_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_db():
    await create_tables()
    print('database created!')


async def drop_db():
    await drop_tables()
    print('database drop!')


def main():
    command = sys.argv[1]
    if command == 'create_db':
        asyncio.run(create_db())
    if command == 'drop_db':
        asyncio.run(drop_db()) 


if __name__ == "__main__":
    main()