from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from advanced_alchemy.base import CommonTableAttributes

class UserModel(CommonTableAttributes):
    """User model."""

    __tablename__ = "user"  # Изменено на "user" согласно заданию

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    