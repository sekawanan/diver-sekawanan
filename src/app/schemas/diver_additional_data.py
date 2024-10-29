# app/schemas/diver_gear.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# Base schema
class DiverAdditionalDataBase(BaseModel):
    id: int
    diver_profile_id: int
    total_dive_log: date
    total_visited_dive_site: date
    created_at: datetime
    modified_at: datetime

# Read schema
class DiverAdditionalDataRead(DiverAdditionalDataBase):

    class Config:
        from_attribute=True