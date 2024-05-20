from src.db.models.mongo_model import MongoModel
from pydantic import constr
from datetime import datetime
from typing import Optional, Dict


class TranslationDB(MongoModel):
    word: constr(max_length=255)
    create_time: datetime
    update_time: datetime
    deleted: bool
    translations: Optional[Dict]


