import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
def read_root():
    return {"Hello": "World"}   
    