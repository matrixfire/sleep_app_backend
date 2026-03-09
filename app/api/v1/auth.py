from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_auth_service
from app.schemas import LoginRequest, Token
from app.services import AuthService

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    data: LoginRequest,
    auth_svc: AuthService = Depends(get_auth_service),
) -> Token:
    """Authenticate an admin user and return a JWT access token."""
    token = auth_svc.authenticate(username=data.username, password=data.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return token

