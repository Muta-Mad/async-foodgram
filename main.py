import uvicorn

from fastapi import FastAPI

from api.exception_handlers import api_exception_handlers
from api.routers import router as api_router

app = FastAPI()

api_exception_handlers(app)

app.include_router(api_router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
