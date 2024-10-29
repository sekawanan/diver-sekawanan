# app/schemas/master_color.py
from pydantic import BaseModel
from datetime import datetime

class MasterColorRead(BaseModel):
    id: int
    label: str
    hex_code: str
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True