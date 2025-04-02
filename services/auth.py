from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from core.security import verify_password, create_access_token, create_refresh_token
from repositories.user import get_user_by_email, create_user
from schemas.user import LoginRequest, TokenResponse, UserCreate


def register_user(db: Session, user_credentials: UserCreate) -> TokenResponse:
    user = get_user_by_email(db, user_credentials.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    if len(user_credentials.password) < 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too short"
        )

    user = create_user(db, user_credentials)
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


def authenticate_user(db: Session, login_data: LoginRequest) -> TokenResponse:
    user = get_user_by_email(db, login_data.email)
    if user is None or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect email or password"
        )

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
