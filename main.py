import uvicorn

from fastapi import FastAPI
from api.routers import router as api_router

from settings import settings

app = FastAPI()
app.include_router(api_router, prefix=settings.api_prefix)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True,)
