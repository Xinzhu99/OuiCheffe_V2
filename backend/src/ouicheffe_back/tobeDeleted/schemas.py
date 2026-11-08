from pydantic import BaseModel


class UserAuth(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserOut(BaseModel):
    name: str
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        orm_mode = True