from typing import Dict
from src.core import settings
from src.db.database import words_collection
from fastapi import HTTPException
import httpx


class GoogleTranslator:

    def __init__(self):
        self.GOOGLE_TRANSLATE_API_URL = settings.GOOGLE_TRANSLATE_API_URL
        self.GOOGLE_API_KEY = settings.GOOGLE_API_KEY

    async def _process_response(self, response, word: str, target_language: str) -> Dict:
        response_data = response.json()
        if "error" in response_data:
            raise HTTPException(status_code=400, detail="Error fetching data from Google Translate API")

        translation = {
            "word": word,
            "translations": {target_language: response_data["data"]["translations"][0]["translatedText"]}
        }

        return translation

    async def translate(self, word: str, target_language: str) -> Dict:
        word_data = await words_collection.find_one({"word": word})
        if word_data:
            return word_data

        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.GOOGLE_TRANSLATE_API_URL,
                params={"q": word, "target": target_language, "key": self.GOOGLE_API_KEY}
            )
            response_data = await self._process_response(response, word, target_language)

            return response_data
