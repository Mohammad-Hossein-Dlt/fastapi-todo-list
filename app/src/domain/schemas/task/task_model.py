from pydantic import BaseModel, Field, model_validator
from beanie import PydanticObjectId
from datetime import datetime, timezone
from app.src.domain.enums import Status, Priority

class TaskModel(BaseModel):
    id: int | PydanticObjectId | None = None
    user_id: int | PydanticObjectId | None = None
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    deadline: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __setattr__(self, name, value):
        now: datetime = datetime.now(timezone.utc)
        super().__setattr__(name, value)
        super().__setattr__("updated_at", now)
