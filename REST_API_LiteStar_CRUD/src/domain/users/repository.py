from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import BeforeAfter, CollectionFilter, LimitOffset
from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from db.models import UserModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(SQLAlchemyAsyncRepository[UserModel]):
    """User repository."""

    model_type = UserModel


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    """Provide a user repository."""
    return UserRepository(session=db_session)
