from datetime import datetime, timedelta, timezone
from ouicheffe_back.core.config import settings
from ouicheffe_back.schema.schema import TokenType, TokenPayload
import jwt
from jwt import decode as jwt_decode, ExpiredSignatureError, InvalidTokenError
from ouicheffe_back.utils.exceptions import CredentialsException, TokenExpiredException


def get_secret_key(token_type: TokenType) -> str:
    if token_type == TokenType.ACCESS:
        return settings.JWT_SECRET_KEY
    return settings.JWT_REFRESH_SECRET_KEY


def generate_jwt_token(data: dict, token_type: TokenType) -> str:
    payload = data.copy()
    if token_type == TokenType.ACCESS:
        expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    else:
        expire_minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES
    issued_at = datetime.now(timezone.utc)
    payload["iat"] = issued_at
    payload["exp"] = issued_at + timedelta(minutes=expire_minutes)
    payload["type"] = token_type.value
    return jwt.encode(payload, get_secret_key(token_type), algorithm=settings.ALGORITHM)


def decode_token(token: str, token_type: TokenType) -> dict:
    try:
        return jwt_decode(token, get_secret_key(token_type), algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpiredException(f"{token_type.value} token has expired")
    except InvalidTokenError:
        raise CredentialsException(f"Invalid {token_type.value} token")


def validate_token(payload: TokenPayload, seconds: int = 30) -> TokenPayload:
    now = datetime.now(timezone.utc).timestamp()
    if payload.iat > now + seconds:
        raise CredentialsException("Token is invalid: it was issued for a future time")
    if payload.exp <= payload.iat:
        raise CredentialsException("Expiration time must be after issuance time")
    return payload


def verify_token(token: str, token_type: TokenType) -> TokenPayload:
    payload = decode_token(token, token_type)
    validated = validate_token(TokenPayload(**payload))
    if validated.type != token_type.value:
        raise CredentialsException(
            f"Invalid token type: expected '{token_type.value}', got '{validated.type}'"
        )
    return validated


def extract_email(payload: TokenPayload) -> str:
    if not payload.sub:
        raise CredentialsException("Token has no subject")
    return payload.sub