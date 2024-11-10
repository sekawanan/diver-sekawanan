# app/schemas/diver_gear.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.master_brand import MasterBrandRead

# Base schema
class DiverGearBase(BaseModel):
    master_brand_id: int
    color: str
    type: str

# Create schema
class DiverGearCreate(DiverGearBase):
    pass

# Update schema
class DiverGearUpdate(BaseModel):
    master_brand_id: Optional[int] = None
    color: Optional[str] = None
    type: Optional[str] = None

# Read schema
class DiverGearRead(DiverGearBase):
    id: int
    color: Optional[str] = None
    brand_label: Optional[str] = None
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True  # Correct for Pydantic v2