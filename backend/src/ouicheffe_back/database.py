import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set (check your .env file)")

# pour se connecter à la BDD et lui communqiuer nos requêtes, il faut passer par un tuyau "engine"
# un pool est un ensemble de connexions réutilisables
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# la classe mère de tous les modèles
Base = declarative_base()



 