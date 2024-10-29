# app/schemas/master_brand.py
from pydantic import BaseModel
from datetime import datetime

class MasterBrandRead(BaseModel):
    id: int
    label: str
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True