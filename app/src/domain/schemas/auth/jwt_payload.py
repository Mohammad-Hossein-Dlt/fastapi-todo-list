from pydantic import BaseModel
from datetime import datetime

class JWTPayload(BaseModel):
    user_id: str
    exp: datetime | None = None