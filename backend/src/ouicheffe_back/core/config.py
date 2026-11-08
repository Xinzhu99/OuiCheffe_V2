from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # extra="ignore" : le .env contient aussi des variables lues ailleurs (DATABASE_URL, CORS_ORIGINS...)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = False
    # origines autorisées à appeler l'API, séparées par des virgules (ex: "https://ouicheffe.fr,https://www.ouicheffe.fr")
    CORS_ORIGINS: str = "http://localhost:5173"
    ASYNC_DATABASE_URL: str
    JWT_SECRET_KEY: str
    # secret distinct pour les refresh tokens : une fuite de l'un ne compromet pas l'autre
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7



settings = Settings()
