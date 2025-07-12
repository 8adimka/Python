from __future__ import annotations
from litestar import Litestar
from db.session import get_async_session, create_db_and_tables
from domain.users.controllers import UserController
from litestar.config.cors import CORSConfig
from litestar.logging import LoggingConfig
import logging

async def on_startup():
    await create_db_and_tables()

def create_app() -> Litestar:
    logging_config=None

    return Litestar(
        route_handlers=[UserController],
        dependencies={"db_session": get_async_session},
        cors_config=CORSConfig(allow_origins=["*"]),
        on_startup=[on_startup],
        logging_config=logging_config,
        debug=True  # Включаем debug режим для диагностики
    )

app = create_app()
