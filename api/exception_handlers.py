from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from api.exceptions import http_exception_handler, validation_exception_handler


def api_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )
    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )
