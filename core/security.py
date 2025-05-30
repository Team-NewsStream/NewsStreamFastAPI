import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from passlib.context import CryptContext

from core.settings import settings

load_dotenv()

JWT_ACCESS_SECRET = settings.JWT_ACCESS_SECRET
JWT_REFRESH_SECRET = settings.JWT_REFRESH_SECRET
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: dict, expires_delta: timedelta, secret: str):
    """Generates a JWT token with a dynamic expiration time."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=secret, algorithm=ALGORITHM)
    return encoded_jwt


def verify_jwt_token(token: str, secret: str):
    """
    Decodes and verifies the given JWT token.

    Returns:
        dict: Decoded token payload if valid.
        None: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(jwt=token, key=secret, algorithms=[ALGORITHM])

        if "exp" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing expiration claim"
            )

        expiration = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
        if datetime.now(timezone.utc) > expiration:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def verify_access_token(token: str):
    """Wrapper function for access token verification."""
    return verify_jwt_token(token, JWT_ACCESS_SECRET)


def verify_refresh_token(token: str):
    """Wrapper function for refresh token verification."""
    return verify_jwt_token(token, JWT_REFRESH_SECRET)


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    """Wrapper to generate an refresh token."""
    if expires_delta:
        return create_jwt_token(data, expires_delta, secret=JWT_REFRESH_SECRET)
    expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return create_jwt_token(data=data, expires_delta=expires_delta, secret=JWT_REFRESH_SECRET)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Wrapper to generate an access token."""
    if expires_delta:
        return create_jwt_token(data, expires_delta, secret=JWT_ACCESS_SECRET)
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_jwt_token(data=data, expires_delta=expires_delta, secret=JWT_ACCESS_SECRET)
