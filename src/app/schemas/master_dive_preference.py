# app/schemas/master_dive_preference.py

from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MasterDivePreferenceBase(BaseModel):
    label: str

    class Config:
        from_attributes = True

class MasterDivePreferenceCreate(MasterDivePreferenceBase):
    pass

class MasterDivePreferenceUpdate(BaseModel):
    label: Optional[str] = None

    class Config:
        from_attributes = True

class MasterDivePreferenceRead(MasterDivePreferenceBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True  # Enables from_orm