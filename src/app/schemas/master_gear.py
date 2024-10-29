# app/schemas/master_gear.py
from pydantic import BaseModel
from datetime import datetime

class MasterGearBase(BaseModel):
    id: int
    label: str
    created_at: datetime
    modified_at: datetime

class MasterGearRead(MasterGearBase):    
    class Config:
        from_attributes = True