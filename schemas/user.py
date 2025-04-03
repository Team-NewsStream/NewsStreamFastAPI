from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str
