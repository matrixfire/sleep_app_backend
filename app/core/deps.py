from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status # Depends means having FastAPI automatically provide this for me
from fastapi.security import OAuth2PasswordBearer # HANDLES Bearer Token
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.schemas import UserWithPerms
from app.services import AuthService
from db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db=db)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],  # Get the bearer token from the request using FastAPI's dependency system
    db: Session = Depends(get_db),                  # Get a database session using FastAPI's dependency injection
) -> UserWithPerms:
    payload = decode_token(token)                   # Decode the JWT access token to get the user's info (payload)
    if payload is None:                             # If the token could not be decoded (invalid/expired)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",   # Let the client know authentication failed
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = int(payload.sub)                      # Extract the user's ID from the token's subject (sub) field
    auth_svc = AuthService(db)                      # Initialize the authentication service with the current DB session
    user = auth_svc.load_current_user(user_id)      # Use the authentication service to get the current user by ID
    if user is None or not user.is_active:          # Check if the user exists and is active
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",                   # Inform client that user is inactive or doesn't exist
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user                                     # Return the authenticated and active user object






'''
1. JWT (JSON Web Token) is a stateless authentication mechanism used to securely transmit information between a client and a server. 
A JWT has three parts: Header, Payload, and Signature.

The payload contains claims such as the user ID and timestamps like iat (issued at) and exp (expiration time). When a user logs in, the server creates the JWT, signs it with a secret key, and sends it to the client.

The client includes the token in the Authorization: Bearer token header for each request. The server verifies the signature and checks the timestamps like exp to ensure the token hasn’t expired before allowing access.

'''