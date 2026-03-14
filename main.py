# Import the FastAPI class for building the application
from fastapi import FastAPI

# Import application settings object
from app.core.config import settings
# Import function to add necessary middlewares to the app
from app.core.middleware import add_middlewares
# Import the API router (which bundles all endpoints)
from app.api.v1.api import api_router


def create_app() -> FastAPI:
    # Instantiate the FastAPI app and set the app's title
    app = FastAPI(title=settings.APP_NAME)
    # Add middleware components (e.g., CORS, error handlers) to the app
    add_middlewares(app)
    # Register/bind all API endpoints under the chosen prefix, e.g. /api/v1
    app.include_router(api_router, prefix=settings.API_V1_STR)
    # Return the fully configured FastAPI application instance
    return app


# Create the app instance which will be used by ASGI servers (e.g., Uvicorn)
app = create_app()
