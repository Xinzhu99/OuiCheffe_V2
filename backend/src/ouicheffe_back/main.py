from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from ouicheffe_back.routers.check_db import db_router
from ouicheffe_back.core.config import settings
from ouicheffe_back.routers.auth import auth_router
from ouicheffe_back.routers.users import user_router
from ouicheffe_back.routers.home import home_router

app = FastAPI()

# gestion cors : le front (Vite, autre port) doit pouvoir appeler l'API
# allow_credentials=True : nécessaire pour que le navigateur envoie/accepte le cookie refresh_token
# (incompatible avec allow_origins=["*"], d'où la liste explicite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(db_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(home_router)

if __name__ == "__main__":
    uvicorn.run('ouicheffe_back.main:app', host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
