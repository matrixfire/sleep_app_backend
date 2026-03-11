from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.schemas import (
    AppUserCreate,
    AppUserOut,
    UserAudioPlaybackCreate,
    UserAudioPlaybackListResponse,
    UserAudioPlaybackOut,
    UserSleepRecordCreate,
    UserSleepRecordListResponse,
    UserSleepRecordOut,
    UserWithPerms,
)
from app.services.user_data import UserDataService
from db.session import get_db

router = APIRouter(prefix="/admin/users", tags=["admin-user-data"])


def get_user_data_service(
    db: Session = Depends(get_db),
    current_user: UserWithPerms = Depends(get_current_user),
) -> UserDataService:
    return UserDataService(db=db, current_user=current_user)


@router.post("", response_model=AppUserOut, status_code=status.HTTP_201_CREATED)
def create_app_user(
    data: AppUserCreate,
    svc: UserDataService = Depends(get_user_data_service),
) -> AppUserOut:
    return svc.create_app_user(data)


@router.get("/{user_id}/sleep-records", response_model=UserSleepRecordListResponse)
def list_sleep_records(
    user_id: int,
    page: int = 1,
    size: int = 20,
    svc: UserDataService = Depends(get_user_data_service),
) -> UserSleepRecordListResponse:
    return svc.list_sleep_records(user_id=user_id, page=page, size=size)


@router.post("/{user_id}/sleep-records", response_model=UserSleepRecordOut, status_code=status.HTTP_201_CREATED)
def create_sleep_record(
    user_id: int,
    data: UserSleepRecordCreate,
    svc: UserDataService = Depends(get_user_data_service),
) -> UserSleepRecordOut:
    return svc.create_sleep_record(user_id=user_id, data=data)


@router.get("/{user_id}/audio-playbacks", response_model=UserAudioPlaybackListResponse)
def list_playbacks(
    user_id: int,
    page: int = 1,
    size: int = 20,
    svc: UserDataService = Depends(get_user_data_service),
) -> UserAudioPlaybackListResponse:
    return svc.list_playbacks(user_id=user_id, page=page, size=size)


@router.post(
    "/{user_id}/audio-playbacks",
    response_model=UserAudioPlaybackOut,
    status_code=status.HTTP_201_CREATED,
)
def create_playback(
    user_id: int,
    data: UserAudioPlaybackCreate,
    svc: UserDataService = Depends(get_user_data_service),
) -> UserAudioPlaybackOut:
    return svc.create_playback(user_id=user_id, data=data)

