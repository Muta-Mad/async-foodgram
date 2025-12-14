from typing import cast

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request,
    exc: Exception,
):
    exc = cast(RequestValidationError, exc)

    errors: dict[str, list[str]] = {}

    for error in exc.errors():
        field = error['loc'][-1]
        if error['type'] == 'missing':
            message = 'Обязательное поле.'
        else:
            message = error['msg']
        errors.setdefault(field, []).append(message)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=errors,
    )

async def http_exception_handler(
    request: Request,
    exc: Exception,
):
    exc = cast(HTTPException, exc)
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'detail': 'Учетные данные не были предоставлены.'
            },
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail},
    )

def not_found_error(eror: str):
    """Вызывает 404 если объект не найден."""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=eror,
    )
