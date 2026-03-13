from fastapi import APIRouter

from app.api.v1 import admin_audio, admin_rbac, admin_daily_quote, admin_stats, admin_user_data, app_api, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(app_api.router)
api_router.include_router(admin_audio.router)
api_router.include_router(admin_rbac.router)
api_router.include_router(admin_daily_quote.router)
api_router.include_router(admin_stats.router)
api_router.include_router(admin_user_data.router)

