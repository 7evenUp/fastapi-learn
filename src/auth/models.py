from datetime import datetime
from sqlalchemy import MetaData, String, Integer, TIMESTAMP, ForeignKey, Table, Column, JSON, Boolean
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey, Column, Boolean
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTable

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON)
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    registered_at: Mapped[str] = mapped_column(
        TIMESTAMP, default=datetime.utcnow)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(
        String(length=1024), nullable=False
    )
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(
        Boolean, default=False, nullable=False
    )
    is_verified: bool = Column(
        Boolean, default=False, nullable=False
    )
