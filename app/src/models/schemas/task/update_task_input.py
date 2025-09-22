from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from app.src.domain.enums import Priority, Status
from datetime import datetime, timezone

class UpdateTaskInput(BaseModel):
    id: int | PydanticObjectId
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    deadline: datetime | None = None