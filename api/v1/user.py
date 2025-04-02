from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.base import get_db
from schemas.user import UserCreate, TokenResponse, LoginRequest
from services.auth import authenticate_user, register_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup", response_model=TokenResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)


@router.post("/login", response_model=TokenResponse)
def login(user_credentials: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(db, user_credentials)
