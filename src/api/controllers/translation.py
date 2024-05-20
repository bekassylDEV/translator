from src.db.dao.translation import get_translation, create_translation
from src.integrations import google_translator
from src.schemas.api.translation import TranslationOut
from src.db.database import words_collection
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Dict, List


class TranslationController:

    """
    In get_translation controller methdod, I use a pattern, where database connection is achieved through dependency injection.
    In other controller methods, I use words_collection directly, without dependency injection.
    This is just to show that both ways are possible.
    """

    async def get_translation(self, db: AsyncIOMotorClient, word: str, target_language: str) -> TranslationOut:
        word_data: Dict = await get_translation(db, word)
        if word_data:
            return TranslationOut(**{k: v for k, v in word_data.items() if k in TranslationOut.__annotations__})

        translation: Dict = await google_translator.translate(word, target_language)

        translation_out = TranslationOut(**translation)
        await create_translation(db, translation_out.dict())

        return translation_out

    async def delete_word(self, db: AsyncIOMotorClient, word: str) -> Dict:
        delete_result = await words_collection.delete_one({"word": word})
        if delete_result.deleted_count == 1:
            return {"status": "Word deleted"}
        raise HTTPException(status_code=404, detail="Word not found")

    async def list_words(self, db: AsyncIOMotorClient, skip: int = 0, limit: int = 10, query: Optional[str] = None) -> List[TranslationOut]:
        query_filter = {"word": {"$regex": query, "$options": "i"}} if query else {}
        cursor = words_collection.find(query_filter).skip(skip).limit(limit)
        words = await cursor.to_list(length=limit)
        list_words = [TranslationOut(**{k: v for k, v in word_data.items() if k in TranslationOut.__annotations__}) for word_data in words]
        return list_words
