# app/schemas/master_marine_life.py
from __future__ import annotations  # Add this line at the very top
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MasterMarineLifeBase(BaseModel):
    id: int
    label: str
    image_url: str
    image_credit: str
    description: Optional[str]
    created_at: datetime
    modified_at: datetime

class MasterMarineLifeRead(MasterMarineLifeBase):    
    class Config:
        from_attributes = True