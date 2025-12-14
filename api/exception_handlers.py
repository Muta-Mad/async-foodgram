from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

from api.exceptions import (
    validation_exception_handler,
    http_exception_handler,
)


def api_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )
    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )
