from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ouicheffe_back.services.auth import AuthService, get_auth_service
from ouicheffe_back.schema.schema import TokenType
from ouicheffe_back.services.users import UserService, get_user_service
from ouicheffe_back.utils.exceptions import CredentialsException, TokenExpiredException
from ouicheffe_back.auth.tokens import generate_jwt_token
from ouicheffe_back.schema.schema import RegisterUserSchema, UserResponse
from ouicheffe_back.utils.exceptions import UserAlreadyExistsException
from ouicheffe_back.core.config import settings
from ouicheffe_back.utils.exceptions import CredentialsException, UserAlreadyExistsException


auth_router = APIRouter(prefix="/auth", tags=["auth"])

# le cookie est envoyé seulement aux routes /auth/... (refresh, logout)
# set_cookie et delete_cookie doivent utiliser les mêmes attributs, sinon le navigateur garde le cookie
REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_ATTRS = {"path": "/auth", "httponly": True, "samesite": "lax", "secure": True}

@auth_router.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
      ):

    current_user = await user_service.get_by_email(email=form_data.username)
    if not current_user:
        raise CredentialsException
    try:
        access_token, refresh_token = await auth_service.authenticate(form_data.password, current_user)
    except CredentialsException as exc:
        raise CredentialsException from exc

    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,   # même durée que le token qu'il contient
        **REFRESH_COOKIE_ATTRS,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/refresh")
async def refresh_token(request: Request, service: AuthService = Depends(get_auth_service)):
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    try:
        user = await service.get_user_from_token(refresh_token, TokenType.REFRESH)
    except TokenExpiredException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
    except CredentialsException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    new_access_token = generate_jwt_token({"sub": user.email}, TokenType.ACCESS)
    return {"access_token": new_access_token, "token_type": "bearer"}


# pas de Depends(get_current_user) : on doit pouvoir se déconnecter même avec un access token expiré
@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key=REFRESH_COOKIE_NAME, **REFRESH_COOKIE_ATTRS)

@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterUserSchema,
    user_service: UserService = Depends(get_user_service),
):
    try:
        return await user_service.register(data)
    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )


