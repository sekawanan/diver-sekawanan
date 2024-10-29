# app/schemas/dive_log.py
from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional
from decimal import Decimal
from datetime import datetime
from enum import Enum

class DiveSuitEnum(str, Enum):
    DRY_SUIT = "Dry Suit"
    WET_SUIT = "Wet Suit"
    OTHER = "Other"

class DiveLogBase(BaseModel):
    diver_profile_id: int
    master_dive_site_id: Optional[int] = None
    master_dive_type_id: Optional[int] = None
    dive_suit: Optional[DiveSuitEnum] = None
    dive_log_date: Optional[datetime] = None
    time_in: Optional[time] = None
    time_out: Optional[time] = None
    max_depth: Optional[int] = None  # smallint in DB, use int


class DiveLogCreate(DiveLogBase):
    pass


class DiveLogUpdate(BaseModel):
    diver_profile_id: Optional[int]
    master_dive_site_id: Optional[int]
    master_dive_type_id: Optional[int]
    dive_suit: Optional[DiveSuitEnum]
    dive_log_date: Optional[datetime]
    time_in: Optional[time]
    time_out: Optional[time]
    max_depth: Optional[int]


class DiveLogRead(DiveLogBase):
    id: int
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

    class Config:
       from_attributes=True  # Important to serialize SQLAlchemy models
