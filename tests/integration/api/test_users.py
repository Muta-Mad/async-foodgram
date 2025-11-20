import pytest
from httpx import AsyncClient


class TestUsersEndpoints:
    """Тесты эндпоинтов пользователей"""

    @pytest.mark.asyncio
    async def test_get_users(self, client: AsyncClient):
        response = await client.get("api/users/")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_create_user_success(self, client: AsyncClient):
        user_data = {
            "email": "test@example.com",
            "first_name": "Test User",
            "last_name": "Test User"
        }

        response = await client.post("api/users/", json=user_data)

        assert response.status_code == 200
