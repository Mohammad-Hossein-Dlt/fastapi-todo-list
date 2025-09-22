from ._base import Base
from app.src.domain.schemas.task.task_model import TaskModel
from app.src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, Enum
from app.src.domain.enums import Status, Priority
from datetime import datetime, timezone

class TaskDBModel(UpdateFromSchemaMixin, Base):
    __tablename__ = "tasks"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(Status), nullable=False)
    priority = Column(Enum(Priority), nullable=False)
    deadline = Column(DateTime, nullable=True, default=None)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
