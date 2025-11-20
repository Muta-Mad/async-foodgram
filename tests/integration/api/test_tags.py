import pytest
from httpx import AsyncClient


class TestTagsEndpoints:
    """Тесты эндпоинтов пользователей"""

    @pytest.mark.asyncio
    async def test_get_tags(self, client: AsyncClient):
        response = await client.get("api/tags/")

        assert response.status_code == 200
