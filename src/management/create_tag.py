import asyncio
import json
import sys
from pathlib import Path

from sqlalchemy import insert

current_dir = Path(__file__).parent
src_path = current_dir.parent
sys.path.insert(0, str(src_path))

from core.database import new_session  # noqa: E402
from models.tag import Tag  # noqa: E402

current_dir = Path(__file__).parent


async def create_tag():
    """ Асинхронная функция для создания тегов """

    json_file = current_dir / "data.json"

    with open(json_file, "r", encoding="utf-8") as file:
        tags_data = [json.loads(line.strip()) for line in file]

    async with new_session() as db:
        stmt = insert(Tag).values(tags_data)
        await db.execute(stmt)
        await db.commit()
    print('Созданы теги')

if __name__ == "__main__":
    asyncio.run(create_tag())
