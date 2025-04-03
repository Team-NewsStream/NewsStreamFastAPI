from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.base import get_db
from schemas.user import UserCreate, TokenResponse, LoginRequest, RefreshTokenRequest
from services.auth import authenticate_user, register_user, refresh_tokens

router = APIRouter(tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)


@router.post("/login", response_model=TokenResponse)
def login(user_credentials: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(db, user_credentials)


@router.get("/refresh", response_model=TokenResponse)
def refresh_token(credentials: RefreshTokenRequest):
    return refresh_tokens(refresh_token=credentials.refresh_token)
