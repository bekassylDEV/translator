import os

from .settings import Settings

settings = Settings(_env_file=os.getenv("ENV_FILE", ""))