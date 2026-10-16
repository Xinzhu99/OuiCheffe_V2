import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import get_db
from sqlalchemy.orm import Session
from .models import Recipe
from .schemas import RecipeOut

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

@app.get("/recipes", response_model=list[RecipeOut])
def read_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).all()
