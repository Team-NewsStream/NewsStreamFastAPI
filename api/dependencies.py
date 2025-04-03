from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.security import verify_access_token
from db.base import get_db
from models.user import User
from repositories.user import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    """Extracts and verifies user from JWT token."""
    payload = verify_access_token(token=token)

    user = get_user_by_email(db, email=payload["sub"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
