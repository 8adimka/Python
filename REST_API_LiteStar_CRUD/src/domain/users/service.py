from __future__ import annotations
from typing import Tuple, List
from litestar.exceptions import NotFoundException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import UserModel
from domain.users.repository import UserRepository

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(session=session)  # Используем наш репозиторий

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

    async def list_and_count(self, limit: int, offset: int) -> Tuple[List[UserModel], int]:
        # Получаем список пользователей
        users = (await self.session.execute(
            select(UserModel).offset(offset).limit(limit)
        )).scalars().all()
        
        # Получаем общее количество
        total = (await self.session.execute(
            select(func.count(UserModel.id))
        )).scalar_one()
        
        return users, total
    