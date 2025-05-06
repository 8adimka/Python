from __future__ import annotations

from datetime import datetime

from litestar.dto import DataclassDTO, DTOConfig
from litestar import post, put, get, delete
from litestar.controller import Controller
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset
from pydantic import BaseModel, Field
from uuid import UUID

from db.models import UserModel, UserService
from db.session import provide_transaction


class UserCreate(BaseModel):
    """User create schema."""

    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=6, max_length=255)


class UserUpdate(BaseModel):
    """User update schema."""

    name: str | None = Field(default=None, min_length=1, max_length=50)
    surname: str | None = Field(default=None, min_length=1, max_length=50)
    password: str | None = Field(default=None, min_length=6, max_length=255)


class UserOut(BaseModel):
    """User output schema."""

    id: int
    name: str
    surname: str
    created_at: datetime
    updated_at: datetime


class UserDTO(DataclassDTO[UserCreate]):
    """User DTO."""

    config = DTOConfig(exclude={"password"})


class UserUpdateDTO(DataclassDTO[UserUpdate]):
    """User update DTO."""

    config = DTOConfig(exclude={"password"}, partial=True)
    