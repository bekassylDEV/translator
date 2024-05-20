from uuid import uuid4
from datetime import datetime, UTC
import logging
from typing import Dict
from pymongo import ReturnDocument

from src.core import settings
from motor.motor_asyncio import AsyncIOMotorClient
from src.schemas.models.translation import TranslationDB


__db_name = settings.DB_NAME
__db_collection = settings.COLLECTION_NAME


async def create_translation(
    conn: AsyncIOMotorClient,
    word: Dict,
) -> TranslationDB:
    new_translation = TranslationDB(
        create_time=datetime.now(UTC),
        update_time=datetime.now(UTC),
        deleted=False,
        **word,

    )
    logging.info(
        f'Inserting sample resource {word} into db.'
    )
    await conn[__db_name][__db_collection].insert_one(
        new_translation.mongo()
    )
    logging.info(
        f"Sample resource {word} has inserted into db"
    )
    return new_translation


async def get_translation(
    conn: AsyncIOMotorClient,
    word: str
) -> Dict | None:
    logging.info(f"Getting translation for word: {word}")
    translation = await conn[__db_name][__db_collection].find_one(
        {"$and": [
            {'word': word},
            {'deleted': False},
        ]},
    )

    if None is translation:
        logging.info(f"Translation for word {word} is None")

    return translation


async def delete_translation(
    conn: AsyncIOMotorClient,
    word: str,
) -> TranslationDB | None:
    logging.info(
        f"Deleting trnalstion for word {word}."
    )

    translation = await conn[__db_name][__db_collection].\
        find_one_and_update(
        {"$and": [
            {'word': word},
            {'deleted': False},
        ]},
        {'$set': {
            "deleted": True,
            "update_time": datetime.now(UTC),
        }},
        return_document=ReturnDocument.AFTER,
    )

    if None is translation:
        logging.error(
            f"Translation for word {word} does not exist."
        )
    else:
        logging.info(
            f'Translation for word {word} was deleted.'
        )
    return translation
