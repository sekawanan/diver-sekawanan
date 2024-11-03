# app/schemas/diver_profile.py
from __future__ import annotations  # Ensure forward references are handled
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date

# Import necessary schemas
from .diver_license import DiverLicenseRead
from .dive_preference import DivePreferenceRead
from .diver_gear import DiverGearRead

class DiverProfileBase(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    full_name: str
    birth_date: date

class DiverProfileCreate(DiverProfileBase):
    """
    Schema for creating a new diver profile.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: str
    birth_date: date

    class Config:
        from_attributes = True  # Correct for Pydantic v2

class DiverProfileCreateResponse(DiverProfileBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True  # Correct for Pydantic v2

class DiverProfileUpdate(BaseModel):
    user_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class DiverProfileRead(DiverProfileBase):
    id: int
    created_at: datetime
    modified_at: datetime
    diver_gears: List[DiverGearRead] = []
    diver_licenses: List[DiverLicenseRead] = []
    dive_preferences: List[DivePreferenceRead] = []

    class Config:
        from_attributes = True  # Correct for Pydantic v2
        populate_by_name = True  # Optional: if you have aliases