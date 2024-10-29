# app/schemas/master_gear_brand.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .master_gear import MasterGearRead
from .master_brand import MasterBrandRead

class MasterGearBrandRead(BaseModel):
    id: int
    master_gear_id: int
    master_gear: MasterGearRead
    gear_label: Optional[str]
    master_brand_id: int
    master_brand: MasterBrandRead
    brand_label: Optional[str]
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True