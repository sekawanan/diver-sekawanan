# app/schemas/diver_license.py
from __future__ import annotations  # Add this line at the very top
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# Import the referenced schema
from .master_license import MasterLicenseRead

# Base schema without diver_profile_id
class DiverLicenseBase(BaseModel):
    id: int
    license_institution: str
    license_level: str
    diver_name: str
    diver_number: str
    birth_date_license: Optional[date] = None
    certificate_date: Optional[date] = None
    instructor_name: Optional[str] = None
    instructor_number: Optional[int] = None
    store_name: Optional[str] = None
    store_number: Optional[int] = None
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

# Create schema
class DiverLicenseCreate(BaseModel):
    license_institution: str
    license_level: str
    diver_name: str
    diver_number: str
    birth_date_license: Optional[date] = None
    certificate_date: Optional[date] = None
    instructor_name: Optional[str] = None
    instructor_number: Optional[int] = None
    store_name: Optional[str] = None
    store_number: Optional[int] = None

    class Config:
        from_attributes = True
        orm_mode = True