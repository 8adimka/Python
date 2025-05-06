from __future__ import annotations
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from lib.settings import settings
from advanced_alchemy import SQLAlchemyAsyncRepository

engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

async def provide_transaction(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with db_session.begin():
        yield db_session
        