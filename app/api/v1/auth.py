from __future__ import annotations  # allow future Python features, like postponed evaluation of type annotations

from fastapi import APIRouter, Depends, HTTPException, status  # import FastAPI tools for building APIs
from sqlalchemy.orm import Session  # import for interacting with databases (not used here, but often in APIs)

from app.core.deps import get_auth_service  # function to get the authentication service
from app.schemas import LoginRequest, Token  # import request and response data models
from app.services import AuthService  # service that handles authentication logic

router = APIRouter(prefix="/auth", tags=["auth"])  # create a router for authentication APIs


@router.post("/login", response_model=Token)  # define POST endpoint for login, returns Token schema
def login(
    data: LoginRequest,  # request body expected to have username and password
    auth_svc: AuthService = Depends(get_auth_service),  # get AuthService instance using dependency injection
) -> Token:  # function returns a Token model
    """Authenticate an admin user and return a JWT access token."""
    token = auth_svc.authenticate(username=data.username, password=data.password)  # try to authenticate user
    if token is None:  # if authentication fails
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # return 401 HTTP error (unauthorized)
            detail="Incorrect username or password",  # error message
        )
    return token  # return the JWT token if login succeeds

