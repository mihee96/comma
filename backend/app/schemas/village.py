from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VillageCreate(BaseModel):
    name: str
    region: str
    description: str = ""


class VillageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    name: str
    region: str
    description: str
    is_verified: bool
    created_at: datetime
