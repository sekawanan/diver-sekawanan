# app/schemas/diver.py
from typing import List
from pydantic import BaseModel
from datetime import datetime

class DiverBase(BaseModel):
    first_name: str
    last_name: str

class DiverWithDetails(DiverBase):
    diver_profile_id: int
    user_id: str
    created_at: datetime
    modified_at: datetime

class DiverWithLicenses(DiverWithDetails):
    licenses: List[DiverLicense]
    dive_preferences: List[DivePreference]

    class Config:
        from_attributes = True