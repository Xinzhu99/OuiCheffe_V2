from enum import Enum
from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPayload(BaseModel):
    sub: str
    exp: float
    iat: float
    type: str


class RegisterUserSchema(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    brigade_id: int
    is_active: bool

    class Config:
        from_attributes = True


class SignInRequest(BaseModel):
    email: str
    password: str


class RegisterUserSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr                                  # rejects "abc" with a 422
    password: str = Field(min_length=8)              # no role, no brigade_id: the client doesn't choose them


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: str
    brigade_id: int
    is_active: bool


class RecipesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    prep_time: int
    servings: int
    image_url: str | None = None   # nullable dans le modèle
    