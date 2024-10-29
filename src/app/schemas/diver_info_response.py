# app/schemas/diver_info_response.py
from __future__ import annotations  # Add this line at the very top
from pydantic import BaseModel
from typing import List
from datetime import datetime

# Import necessary schemas
from .diver_profile import DiverProfileRead
from .diver_license import DiverLicenseRead
from .dive_preference import DivePreferenceRead
from .diver_gear import DiverGearRead

class DiverInfoData(BaseModel):
    profile: DiverProfileRead
    diver_licenses: List[DiverLicenseRead] = []
    dive_preferences: List[DivePreferenceRead] = []
    diver_gears: List[DiverGearRead] = []

    class Config:
        from_attributes = True

class DiverInfoResponse(BaseModel):
    status: str
    message: str
    data: DiverInfoData

    class Config:
        from_attributes = True