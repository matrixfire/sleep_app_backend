from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.models import AudioResource
from app.schemas import AudioCreate, AudioListResponse, AudioOut, AudioUpdate, UserWithPerms

PERM_AUDIO_READ = "audio:read"
PERM_AUDIO_CREATE = "audio:create"
PERM_AUDIO_UPDATE = "audio:update"
PERM_AUDIO_DELETE = "audio:delete"


def _ensure_permission(user: UserWithPerms, perm_code: str) -> None:
    if perm_code not in user.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing permission: {perm_code}",
        )


class AudioService:
    def __init__(self, db: Session, current_user: UserWithPerms):
        self.db = db
        self.current_user = current_user

    def list_audios(self, page: int, size: int) -> AudioListResponse:
        _ensure_permission(self.current_user, PERM_AUDIO_READ)
        total, items = crud.list_audios(self.db, page=page, size=size)
        return AudioListResponse(
            total=total,
            items=[AudioOut.model_validate(obj) for obj in items],
        )

    def create_audio(self, data: AudioCreate) -> AudioOut:
        _ensure_permission(self.current_user, PERM_AUDIO_CREATE)
        obj = AudioResource(
            title=data.title,
            cover_url=str(data.cover_url) if data.cover_url is not None else None,
            audio_url=str(data.audio_url),
        )
        obj = crud.create_audio(self.db, obj)
        return AudioOut.model_validate(obj)

    def update_audio(self, audio_id: int, data: AudioUpdate) -> AudioOut:
        _ensure_permission(self.current_user, PERM_AUDIO_UPDATE)
        obj = crud.get_audio(self.db, audio_id=audio_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found")
        if data.title is not None:
            obj.title = data.title
        if data.cover_url is not None:
            obj.cover_url = str(data.cover_url)
        if data.audio_url is not None:
            obj.audio_url = str(data.audio_url)
        obj = crud.update_audio(self.db, obj)
        return AudioOut.model_validate(obj)

    def delete_audio(self, audio_id: int) -> None:
        _ensure_permission(self.current_user, PERM_AUDIO_DELETE)
        obj = crud.get_audio(self.db, audio_id=audio_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found")
        crud.delete_audio(self.db, obj)

