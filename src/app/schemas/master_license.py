# app/schemas/master_license.py
from __future__ import annotations  # Add this line at the very top
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MasterLicenseRead(BaseModel):
    id: int
    title: str
    type: str
    issuer: str
    alias: Optional[str] = None
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True