from motor.motor_asyncio import AsyncIOMotorClient
from src.core import settings
import logging

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DB_NAME]
words_collection = db["words"]
words_collection.create_index([('word', 'text')])

db_client: AsyncIOMotorClient = None


async def get_db() -> AsyncIOMotorClient:
    return db_client


async def connect_to_db():
    logging.info('Connecting to MongoDB. Please, wait!')
    global db_client
    db_client = AsyncIOMotorClient(
        settings.MONGODB_URL
    )
    logging.info('Connected to MongoDB.')


async def close_db_connect():
    logging.info('Closing connection to MongoDB.')
    global db_client
    db_client.close()
    logging.info('MongoDB connection closed.')
