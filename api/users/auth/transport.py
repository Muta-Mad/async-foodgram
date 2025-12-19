from fastapi import Request
from fastapi_users.authentication import BearerTransport


class TokenTransport(BearerTransport):
    scheme_name: str = 'Token'

    async def __call__(self, request: Request) -> str | None:
        auth = request.headers.get('Authorization')
        if not auth:
            return None
        scheme, _, token = auth.partition(' ')
        if scheme.lower() != 'token' or not token:
            return None
        return token

token_transport = TokenTransport(tokenUrl='/api/auth/token/login')