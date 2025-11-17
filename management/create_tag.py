import asyncio
from pathlib import Path
import json
import sys

from api.models import Tag
from api.database import new_session

current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))


async def create_tag():
    """ Асинхронная функция для создания тегов """

    json_file = current_dir / "data.json"

    with open(json_file, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line.strip())
            async with new_session() as db:
                tag = Tag(
                    name=data["name"],
                    slug=data["slug"],
                )
                db.add(tag)
                await db.commit()
                await db.refresh(tag)
                print(f'Тег создан с id {tag.id}')

asyncio.run(create_tag())
