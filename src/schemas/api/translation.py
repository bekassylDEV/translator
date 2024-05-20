from pydantic import BaseModel
from typing import Optional, Dict


class TranslationOut(BaseModel):
    word: Optional[str]
    translations: Optional[Dict]
