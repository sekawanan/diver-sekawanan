# app/schemas/dive_preference.py

from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from .master_dive_preference import MasterDivePreferenceRead

class DivePreferenceBase(BaseModel):
    master_dive_preference_id: int

    class Config:
        from_attributes = True

# Schema for creating a single dive preference
class DivePreferenceCreate(BaseModel):
    master_dive_preference_id: int

# Schema for creating multiple dive preferences
class DivePreferenceCreateMultiple(BaseModel):
    master_dive_preference_ids: List[int]

# Schema for updating an existing dive preference
class DivePreferenceUpdate(BaseModel):
    master_dive_preference_id: Optional[int] = None

    class Config:
        from_attributes = True

# Schema for reading dive preferences
class DivePreferenceRead(BaseModel):
    id: int
    diver_profile_id: int
    master_preference: MasterDivePreferenceRead
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True  # Enables from_orm
