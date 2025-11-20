import pytest
from httpx import AsyncClient


class TestIngredientsEndpoints:
    """Тесты эндпоинтов пользователей"""

    @pytest.mark.asyncio
    async def test_get_ingredients(self, client: AsyncClient):
        response = await client.get("api/ingredients/")

        assert response.status_code == 200
