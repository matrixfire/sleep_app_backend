from fastapi import FastAPI

from app.core.config import settings
from app.core.middleware import add_middlewares
from app.api.v1.api import api_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)
    add_middlewares(app)
    app.include_router(api_router, prefix=settings.API_V1_STR)
    return app


app = create_app()

