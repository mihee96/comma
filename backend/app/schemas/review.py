from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    village_id: int
    rating: int = Field(ge=1, le=5, default=5)
    content: str = ""


class ReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    village_id: int
    user_id: int
    rating: int
    content: str
    created_at: datetime
