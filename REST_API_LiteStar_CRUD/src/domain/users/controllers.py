from __future__ import annotations

from typing import TYPE_CHECKING

from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset

from domain.users.dtos import UserCreate, UserUpdate, UserOut
from domain.users.service import UserService
from db.session import get_async_session, provide_transaction

class UserController(Controller):
    """User controller."""

    path = "/users"
    dependencies = {
        "user_service": Provide(UserService),
        "transaction": Provide(provide_transaction),
    }
    return_dto = None  # Упрощаем для примера

    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserOut:
        """Create a new user."""
        user = await user_service.create(data.model_dump())
        return UserOut.model_validate(user)

    @get()
    async def list_users(
        self,
        user_service: UserService,
        limit_offset: LimitOffset,
    ) -> OffsetPagination[UserOut]:
        """List users."""
        users, total = await user_service.list_and_count(limit_offset)
        return OffsetPagination[UserOut](
            items=[UserOut.model_validate(user) for user in users],
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @get("/{id:int}")
    async def get_user(
        self,
        user_service: UserService,
        id: int = Parameter(title="User ID", description="The ID of the user to retrieve"),
    ) -> UserOut:
        """Get a user by ID."""
        user = await user_service.get_user(id)
        return UserOut.model_validate(user)

    @put("/{id:int}")
    async def update_user(
        self,
        user_service: UserService,
        data: UserUpdate,
        id: int = Parameter(title="User ID", description="The ID of the user to update"),
    ) -> UserOut:
        """Update a user."""
        user = await user_service.get_user(id)
        updated_user = await user_service.update(user, data.model_dump(exclude_unset=True))
        return UserOut.model_validate(updated_user)

    @delete("/{id:int}")
    async def delete_user(
        self,
        user_service: UserService,
        id: int = Parameter(title="User ID", description="The ID of the user to delete"),
    ) -> None:
        """Delete a user."""
        user = await user_service.get_user(id)
        await user_service.delete(user)
        