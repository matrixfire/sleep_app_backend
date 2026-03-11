from __future__ import annotations # MEANS: Don't rush to check the type name, wait until you've read the whole file first.

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
    """Raise a 403 error if the current user lacks the given permission code."""
    if perm_code not in user.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing permission: {perm_code}",
        )


class AudioService:
    """Service layer for admin audio CRUD with RBAC checks."""

    def __init__(self, db: Session, current_user: UserWithPerms):
        self.db = db
        self.current_user = current_user

    def list_audios(self, page: int, size: int) -> AudioListResponse:
        """Return a paginated list of audios after verifying read permission."""
        _ensure_permission(self.current_user, PERM_AUDIO_READ)
        total, items = crud.list_audios(self.db, page=page, size=size)
        return AudioListResponse(
            total=total,
            items=[AudioOut.model_validate(obj) for obj in items],
        )

    def create_audio(self, data: AudioCreate) -> AudioOut:
        """Create a new audio resource after verifying create permission."""
        _ensure_permission(self.current_user, PERM_AUDIO_CREATE)
        obj = AudioResource(
            title=data.title,
            cover_url=str(data.cover_url) if data.cover_url is not None else None,
            audio_url=str(data.audio_url),
        )
        obj = crud.create_audio(self.db, obj)
        return AudioOut.model_validate(obj)

    def update_audio(self, audio_id: int, data: AudioUpdate) -> AudioOut:
        """Update an existing audio resource after verifying update permission."""
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
        """Delete an audio resource after verifying delete permission."""
        _ensure_permission(self.current_user, PERM_AUDIO_DELETE)
        obj = crud.get_audio(self.db, audio_id=audio_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found")
        crud.delete_audio(self.db, obj)


    def delete_audio_(self, audio_id: int) -> None:
        """Delete an audio resource after verifying delete permission AND ownership."""
        
        # STEP 1: The "Bouncer" check. Does the user have the general ability to delete?
        _ensure_permission(self.current_user, PERM_AUDIO_DELETE)

        # STEP 2: Get the specific data row (the audio file).
        obj = crud.get_audio(self.db, audio_id=audio_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found")

        # --- THIS IS THE NEW, FINE-GRAINED CHECK (The "Floor Manager") ---
        
        # Check if the current user is a SUPER_ADMIN. They can bypass ownership checks.
        is_super_admin = any(role.role_code == "SUPER_ADMIN" for role in self.current_user.roles)

        # If the user is NOT the uploader AND they are NOT a super admin...
        if obj.uploader_id != self.current_user.id and not is_super_admin:
            # ...then deny access.
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete audio you did not upload.",
            )
        
        # --- END OF FINE-GRAINED CHECK ---

        # STEP 3: If all checks pass, proceed with the deletion.
        crud.delete_audio(self.db, obj)


'''
The current MVP implements coarse permissions. Fine-grained is the next step and fits naturally in the service layer.”

'''