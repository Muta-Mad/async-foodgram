from fastapi_users.authentication import BearerTransport

"""Транспорт для BearerToken"""
bearer_transport = BearerTransport(
    tokenUrl='/auth/token/login'
    )
