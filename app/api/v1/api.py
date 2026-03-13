from fastapi import APIRouter

from app.api.v1 import admin_audio, admin_rbac, admin_user_data, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(admin_audio.router)
api_router.include_router(admin_rbac.router)
api_router.include_router(admin_user_data.router)

