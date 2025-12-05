from fastapi_users.authentication import BearerTransport

"""Транспорт для BearerToken"""
bearer_transport = BearerTransport(
    tokenUrl='api/auth/login'
    )

