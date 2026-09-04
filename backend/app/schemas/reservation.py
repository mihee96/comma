from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.reservation import ReservationStatus


class ReservationCreate(BaseModel):
    village_id: int
    start_date: date
    end_date: date
    party_size: int = 1
    note: Optional[str] = None


class ReservationStatusUpdate(BaseModel):
    status: ReservationStatus


class ReservationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    village_id: int
    status: ReservationStatus
    start_date: date
    end_date: date
    party_size: int
    note: Optional[str]
    created_at: datetime
