from typing import Callable
from src.db.database import close_db_connect, connect_to_db


def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        await connect_to_db()

    return start_app


def create_stop_app_handler() -> Callable:
    async def stop_app() -> None:
        await close_db_connect()

    return stop_app
