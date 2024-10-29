# app/schemas/master_dive_site.py
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from datetime import datetime

class MasterDiveSiteRead(BaseModel):
    id: int
    label: str
    latitude: Decimal = Field(..., max_digits=10, decimal_places=8)
    longitude: Decimal = Field(..., max_digits=11, decimal_places=8)
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True