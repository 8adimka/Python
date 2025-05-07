from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=6, max_length=255)

class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    surname: str | None = Field(default=None, min_length=1, max_length=50)
    password: str | None = Field(default=None, min_length=6, max_length=255)

class UserOut(BaseModel):
    id: int
    name: str
    surname: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, user):
        return cls(
            id=user.id,
            name=user.name,
            surname=user.surname,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    