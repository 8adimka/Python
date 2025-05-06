from __future__ import annotations

from litestar import Litestar
from db.session import get_async_session  
from domain.users.controllers import UserController
from litestar.config.cors import CORSConfig

def create_app() -> Litestar:
    return Litestar(
        route_handlers=[UserController],
        dependencies={"db_session": get_async_session},
        cors_config=CORSConfig(allow_origins=["*"]),
    )

app = create_app()
