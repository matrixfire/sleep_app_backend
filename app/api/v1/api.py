from fastapi import APIRouter

from app.api.v1 import admin_audio, admin_user_data, auth, iot

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(admin_audio.router)
api_router.include_router(admin_user_data.router)
api_router.include_router(iot.router)

