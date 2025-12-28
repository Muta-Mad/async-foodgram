import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.core.exception_handlers import api_exception_handlers
from api.routers import router as api_router
from api.core.settings import settings


app = FastAPI()
app.include_router(api_router, prefix='/api')

api_exception_handlers(app)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=settings.cors.allow_credentials,
    allow_origins=settings.cors.allow_origins,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host=settings.app.host, 
        port=settings.app.port, 
        reload=settings.app.reload
    )
