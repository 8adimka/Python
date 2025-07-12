from __future__ import annotations
from typing import AsyncGenerator
from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.pagination import ClassicPagination
from sqlalchemy.ext.asyncio import AsyncSession
from domain.users.dtos import UserCreate, UserUpdate, UserOut
from domain.users.service import UserService
from domain.users.repository import provide_user_repo
from db.session import get_async_session

async def provide_user_service(db_session: AsyncSession) -> UserService:
    return UserService(db_session)

class UserController(Controller):
    path = "/users"
    dependencies = {
        "user_service": Provide(provide_user_service),
    }

    @get("/health")
    async def health_check(self) -> dict:
        return {"status": "ok"}

    @post()
    async def create_user(self, user_service: UserService, data: UserCreate) -> UserOut:
        user = await user_service.create(data.model_dump())
        return UserOut.from_orm(user)

    @get()
    async def list_users(
        self,
        user_service: UserService,
        page: int = 1,
        page_size: int = 10
    ) -> ClassicPagination[UserOut]:
        offset = (page - 1) * page_size
        users, total = await user_service.list_and_count(page_size, offset)
        return ClassicPagination[UserOut](
            items=[UserOut.from_orm(user) for user in users],  # Исправлено здесь
            page_size=page_size,
            current_page=page,
            total_pages=(total + page_size - 1) // page_size
        )

    @get("/{id:int}")
    async def get_user(self, user_service: UserService, id: int) -> UserOut:
        user = await user_service.get_user(id)
        return UserOut.from_orm(user)  # Исправлено здесь

    @put("/{id:int}")
    async def update_user(self, user_service: UserService, data: UserUpdate, id: int) -> UserOut:
        user = await user_service.get_user(id)
        updated_user = await user_service.update(user, data.model_dump(exclude_unset=True))
        return UserOut.from_orm(updated_user)  # Исправлено здесь

    @delete("/{id:int}")
    async def delete_user(self, user_service: UserService, id: int) -> None:
        user = await user_service.get_user(id)
        await user_service.delete(user)
        