from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.models import AppUser, UserAudioPlayback, UserSleepRecord
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

PERM_APP_USER_CREATE = "app_user:create"
PERM_APP_USER_READ = "app_user:read"
PERM_SLEEP_RECORD_CREATE = "sleep_record:create"
PERM_SLEEP_RECORD_READ = "sleep_record:read"
PERM_PLAYBACK_CREATE = "audio_playback:create"
PERM_PLAYBACK_READ = "audio_playback:read"


def _ensure_permission(user: UserWithPerms, perm_code: str) -> None:
    if perm_code not in user.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing permission: {perm_code}",
        )


class UserDataService:
    """Admin-facing service for app-user business data, protected by RBAC."""

    def __init__(self, db: Session, current_user: UserWithPerms):
        self.db = db
        self.current_user = current_user

    def create_app_user(self, data: AppUserCreate) -> AppUserOut:
        _ensure_permission(self.current_user, PERM_APP_USER_CREATE)
        nickname = data.nickname or ("SleepUser_" + uuid.uuid4().hex[:8])
        obj = AppUser(
            mobile=data.mobile,
            nickname=nickname,
            device_sn=data.device_sn,
            device_mac=getattr(data, "device_mac", None),
            wechat_openid=getattr(data, "wechat_openid", None),
        )
        obj = crud.create_app_user(self.db, obj)
        return AppUserOut.model_validate(obj)

    def list_sleep_records(self, user_id: int, page: int, size: int) -> UserSleepRecordListResponse:
        _ensure_permission(self.current_user, PERM_SLEEP_RECORD_READ)
        total, items = crud.list_sleep_records_for_user(self.db, user_id=user_id, page=page, size=size)
        return UserSleepRecordListResponse(
            total=total,
            items=[UserSleepRecordOut.model_validate(x) for x in items],
        )

    def create_sleep_record(self, user_id: int, data: UserSleepRecordCreate) -> UserSleepRecordOut:
        _ensure_permission(self.current_user, PERM_SLEEP_RECORD_CREATE)
        if crud.get_app_user(self.db, user_id=user_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App user not found")
        obj = UserSleepRecord(
            user_id=user_id,
            device_sn=data.device_sn,
            start_time=data.start_time,
            end_time=data.end_time,
            raw_data_url=str(data.raw_data_url),
            analysis_result=data.analysis_result,
        )
        obj = crud.create_sleep_record(self.db, obj)
        return UserSleepRecordOut.model_validate(obj)

    def list_playbacks(self, user_id: int, page: int, size: int) -> UserAudioPlaybackListResponse:
        _ensure_permission(self.current_user, PERM_PLAYBACK_READ)
        total, items = crud.list_playbacks_for_user(self.db, user_id=user_id, page=page, size=size)
        return UserAudioPlaybackListResponse(
            total=total,
            items=[UserAudioPlaybackOut.model_validate(x) for x in items],
        )

    def create_playback(self, user_id: int, data: UserAudioPlaybackCreate) -> UserAudioPlaybackOut:
        _ensure_permission(self.current_user, PERM_PLAYBACK_CREATE)
        if crud.get_app_user(self.db, user_id=user_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App user not found")
        if crud.get_audio(self.db, audio_id=data.audio_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found")
        obj = UserAudioPlayback(
            user_id=user_id,
            audio_id=data.audio_id,
            listened_at=data.listened_at,
            listened_seconds=data.listened_seconds,
            device_sn=data.device_sn,
        )
        obj = crud.create_playback(self.db, obj)
        return UserAudioPlaybackOut.model_validate(obj)

