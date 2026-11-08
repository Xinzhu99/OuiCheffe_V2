from fastapi import Depends, HTTPException, status
from ouicheffe_back.schema.schema import TokenType
from ouicheffe_back.services.auth import AuthService, get_auth_service
from ouicheffe_back.utils.exceptions import CredentialsException, TokenExpiredException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
):
    # sans ce try, une exception Python non gérée remonterait en 500 au lieu de 401
    try:
        user = await auth_service.get_user_from_token(token, TokenType.ACCESS)
    except (CredentialsException, TokenExpiredException) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.detail,
            headers={"WWW-Authenticate": "Bearer"},  # exigé par la norme OAuth2 pour un 401
        ) from exc
    # un compte désactivé ne doit plus accéder à l'API, même avec un token encore valide
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user
