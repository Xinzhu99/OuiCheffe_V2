import os
from sqlite3 import OperationalError
from argon2 import verify_password
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
#from .schemas import UserOut, UserAuth
from ..db.database import Base, get_db
from .models import models
from .utils import get_hashed_password, verify_password
from uuid import uuid4
from sqlalchemy.orm import Session
from .tobeDeleted import schemas
import sqlalchemy as sa

load_dotenv()

app = FastAPI()

#gestion cors
# CORS_ORIGINS : liste d'origines autorisées séparées par des virgules (ex: "https://ouicheffe.fr,https://www.ouicheffe.fr")
# par défaut on garde l'origine de dev Vite pour ne rien casser en local
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"Hello": "World"}   


@app.post('/signup', summary="Create new user", response_model=schemas.UserOut)
async def create_user(data: schemas.UserRegister, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    brigade = models.Brigade()
    db.add(brigade)
    db.flush()  # Flush to get the brigade ID

    user = models.User(
        name=data.name,
        email=data.email,
        hashed_password=get_hashed_password(data.password),
        is_active=True,
        is_superuser=False,
        is_verified=False,
        brigade_id=brigade.id
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post('/login', summary="Login user", response_model=schemas.UserOut)
async def login_user(data: schemas.UserAuth, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
    return user

@app.get("/api/db-healthchecker")
def db_healthchecker(db: Session = Depends(get_db)):
    try:
        # Attempt to execute a simple query to check database connectivity
        db.execute(sa.text("SELECT 1"))
        return {"message": "Database is healthy"}
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database is not reachable")