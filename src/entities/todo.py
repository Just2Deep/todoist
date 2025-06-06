import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import Mapped, mapped_column

from src.database.core import Base


class Priority(Enum):
    NORMAL = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    TOP = 4


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    description: Mapped[str] = mapped_column(String, nullable=False)
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[Priority] = mapped_column(
        ENUM(Priority), nullable=False, default=Priority.NORMAL
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Todo(description={self.description}, due_date={self.due_date})>"
