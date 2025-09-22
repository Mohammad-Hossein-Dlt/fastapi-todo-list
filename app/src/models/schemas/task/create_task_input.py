from pydantic import BaseModel, Field
from app.src.domain.enums import Status, Priority
from datetime import datetime, timezone, timedelta

class CreateTaskInput(BaseModel):
    title: str
    description: str
    status: Status
    priority: Priority
    deadline: datetime | None = None
