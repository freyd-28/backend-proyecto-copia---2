import os

from dotenv import load_dotenv


# Cargar variables del archivo .env
load_dotenv()


def env_bool(name, default=False):
    """Convierte una variable de entorno en booleano."""

    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "true","1", "yes", "y","on", "t",
    }


class Config:
   

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "billeterapp-development-secret-change-in-production-2026",
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        SECRET_KEY,
    )

  

    API_BASE_URL = os.getenv(
        "API_BASE_URL",
        "http://localhost:5000/api/v1",
    ).rstrip("/")

   

    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):

    DEBUG = env_bool(
        "DEBUG",
        True,
    )


class ProductionConfig(Config):

    DEBUG = False


config = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}