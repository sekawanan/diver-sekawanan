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
    master_license_id: int
    certification_number: str
    certificate_date: date
    birth_date_license: Optional[date]
    instructor_name: Optional[str]
    instructor_number: Optional[int]
    store_name: Optional[str]
    store_number: Optional[int]
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True

# Create schema
class DiverLicenseCreate(BaseModel):
    master_license_id: int
    certification_number: str
    certificate_date: Optional[date] = None
    birth_date_license: Optional[date] = None
    instructor_name: Optional[str] = None
    instructor_number: Optional[int] = None
    store_name: Optional[str] = None
    store_number: Optional[int] = None

    class Config:
        from_attributes = True

# Update schema
class DiverLicenseUpdate(BaseModel):
    master_license_id: Optional[int] = None
    certification_number: Optional[str] = None
    certificate_date: Optional[date] = None
    birth_date_license: Optional[date] = None
    instructor_name: Optional[str] = None
    instructor_number: Optional[int] = None
    store_name: Optional[str] = None
    store_number: Optional[int] = None

    class Config:
        from_attributes = True

# Read schema with alias fields for related master_license attributes
class DiverLicenseRead(DiverLicenseBase):
    id: int
    diver_profile_id: int
    master_license: Optional[MasterLicenseRead] = None  # Forward reference using string
    created_at: datetime
    modified_at: datetime
    
    class Config:
        from_attributes = True  # This enables the use of from_orm
        populate_by_name = True  # Pydantic V2: replaces allow_population_by_field_name