import uvicorn

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from api.exceptions import validation_exception_handler, http_exception_handler
from api.routers import router as api_router

app = FastAPI()

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)
app.add_exception_handler(
    HTTPException,
    http_exception_handler
)
app.include_router(api_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
