import asyncio
import json
import sys

from pathlib import Path

from sqlalchemy import exists, insert, select

current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from api.ingredients.models import Ingredient
from api.tags.models import Tag
from database import new_session

PATH_TO_TAGS_DATA = current_dir / 'tags_data.json'
PATH_TO_INGREDIENTS_DATA = current_dir / 'ingredients_data.json'


def get_data(path):
    """
    Получение списка данных.
    Конвертирует json-массив в список словарей с данными.
    """

    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


async def create_objects(model, data):
    """
    Функция для создания объектов.
    Перед созданием проходит проверку на существование записей в базе.
    Если записи существуют, новые записи созданы не будут.
    """
    async with new_session() as db:
        result = await db.execute(select(exists().select_from(model)))
        objects_exists = result.scalar_one_or_none()

        if objects_exists:
            return print(f'Объекты {model.__name__} уже существуют в базе!')

        await db.execute(
            insert(model),
            data,
        )
        await db.commit()
        print(f'Успешно создано {len(data)} объектов {model.__name__}!')


async def main():
    await create_objects(Tag, get_data(PATH_TO_TAGS_DATA))
    await create_objects(Ingredient, get_data(PATH_TO_INGREDIENTS_DATA))


asyncio.run(main())
