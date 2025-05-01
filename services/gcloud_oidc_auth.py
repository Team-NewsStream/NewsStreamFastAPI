import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode, PyJWKClient

from core.settings import settings

security = HTTPBearer()
JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
ISSUER = "https://accounts.google.com"
AUDIENCE = settings.SCHEDULER_AUDIENCE

jwks_client = PyJWKClient(JWKS_URL)


async def verify_internal_service_token(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(credentials.credentials)
        payload = decode(
            credentials.credentials,
            signing_key.key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=ISSUER
        )
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid service token")
