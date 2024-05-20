from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    DEBUG: bool = False
    DOCS_URL: str = "/docs"
    OPENAPI_PREFIX: str = ""
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"

    MONGODB_URL: str
    DB_NAME: str
    COLLECTION_NAME: str

    GOOGLE_TRANSLATE_API_URL: str
    GOOGLE_API_KEY: str

    TESTING: bool = False
    LOG_LEVEL: str = "INFO"

    API_PREFIX: str = "/api"

    BACKEND_CORS_ORIGINS: List[str] = []
    PORT: int = 8080

    class Config:
        case_sensitive = True


class AppSettings(BaseModel):
    BASE_DIR: Path = Path(__file__).absolute().parent.parent

    PROJECT_NAME: str = "translator"
    VERSION: str = "1.0.0"


class Settings(EnvSettings, AppSettings):
    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.DEBUG,
            "docs_url": self.DOCS_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "title": self.PROJECT_NAME,
            "version": self.VERSION,
        }
