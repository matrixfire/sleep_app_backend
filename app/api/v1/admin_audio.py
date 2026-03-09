from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.schemas import AudioCreate, AudioListResponse, AudioOut, AudioUpdate, UserWithPerms
from app.services import AudioService
from db.session import get_db

router = APIRouter(prefix="/admin/audios", tags=["admin-audio"])


def get_audio_service(
    db: Session = Depends(get_db),
    current_user: UserWithPerms = Depends(get_current_user),
) -> AudioService:
    return AudioService(db=db, current_user=current_user)


@router.get("", response_model=AudioListResponse)
def list_audios(
    page: int = 1,
    size: int = 20,
    svc: AudioService = Depends(get_audio_service),
) -> AudioListResponse:
    return svc.list_audios(page=page, size=size)


@router.post("", response_model=AudioOut, status_code=status.HTTP_201_CREATED)
def create_audio(
    data: AudioCreate,
    svc: AudioService = Depends(get_audio_service),
) -> AudioOut:
    return svc.create_audio(data)


@router.put("/{audio_id}", response_model=AudioOut)
def update_audio(
    audio_id: int,
    data: AudioUpdate,
    svc: AudioService = Depends(get_audio_service),
) -> AudioOut:
    return svc.update_audio(audio_id=audio_id, data=data)


@router.delete("/{audio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audio(
    audio_id: int,
    svc: AudioService = Depends(get_audio_service),
) -> Response:
    svc.delete_audio(audio_id=audio_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

