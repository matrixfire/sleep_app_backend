from fastapi import APIRouter  # Import the APIRouter class to create modular API routes

# Import all route modules for version 1 of API (includes admin modules and app module)
from app.api.v1 import (
    admin_audio,         # Admin module for handling audio-related endpoints
    admin_rbac,          # Admin module for RBAC (role-based access control) endpoints
    admin_daily_quote,   # Admin module for managing daily quotes
    admin_stats,         # Admin module for statistics endpoints
    admin_user_data,     # Admin module for user data management
    app_api,             # The app user-facing API routes
    auth,                # Authentication-related endpoints
)

api_router = APIRouter()  # Create the main router for version 1 of the API

api_router.include_router(auth.router, prefix="/auth")  # Mount the authentication routes under the '/auth' path
api_router.include_router(app_api.router)
api_router.include_router(admin_audio.router)
api_router.include_router(admin_rbac.router)
api_router.include_router(admin_daily_quote.router)
api_router.include_router(admin_stats.router)
api_router.include_router(admin_user_data.router)

