from __future__ import annotations
from typing import TYPE_CHECKING
from litestar.exceptions import NotFoundException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import UserModel

if TYPE_CHECKING:
    from litestar.pagination import OffsetPagination

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> UserModel:
        user = UserModel(**data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user(self, id: int) -> UserModel:
        user = await self.session.get(UserModel, id)
        if not user:
            raise NotFoundException("User not found")
        return user

    async def update(self, user: UserModel, data: dict) -> UserModel:
        for key, value in data.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user: UserModel) -> None:
        await self.session.delete(user)
        await self.session.commit()

    async def list_and_count(self, limit_offset) -> tuple[list[UserModel], int]:
        result = await self.session.execute(
            select(UserModel)
            .offset(limit_offset.offset)
            .limit(limit_offset.limit)
        )
        total = await self.session.scalar(select(UserModel).count())
        return result.scalars().all(), total
    