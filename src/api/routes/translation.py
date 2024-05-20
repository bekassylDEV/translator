from fastapi import APIRouter, Depends
from src.api.controllers.translation import TranslationController
from src.schemas.api.translation import TranslationOut
from motor.motor_asyncio import AsyncIOMotorClient
from src.db.database import get_db
from typing import Optional

router = APIRouter(tags=["translation"])

translation_controller = TranslationController()


@router.get("/words")
async def list_words(
        skip: int = 0,
        limit: int = 3,
        query: Optional[str] = None,
        db: AsyncIOMotorClient = Depends(get_db)
):
    return await translation_controller.list_words(db, skip, limit, query)


@router.get("/{word}", response_model=TranslationOut)
async def get_word_details(
        word: str,
        target_language: Optional[str] = "en",
        db: AsyncIOMotorClient = Depends(get_db)
):
    return await translation_controller.get_translation(db, word, target_language)


@router.delete("/{word}")
async def delete_word(
        word: str,
        db: AsyncIOMotorClient = Depends(get_db)
):
    return await translation_controller.delete_word(db, word)
