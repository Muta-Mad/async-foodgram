from typing import Dict, Any
from fastapi_users.authentication import BearerTransport

class Bearer(BearerTransport):
    async def get_login_response(self, token: str) -> Dict[str, Any]:
        return {'auth_token': token}

bearer_transport = Bearer(tokenUrl='auth/token/login')