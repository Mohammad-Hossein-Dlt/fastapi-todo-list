from pydantic import BaseModel

class LoginUserOutput(BaseModel):
    access_token: str