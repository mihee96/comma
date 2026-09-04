from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
