# app/schemas/master_brand.py
from pydantic import BaseModel
from datetime import datetime

class MasterBrandBase(BaseModel):
    label: str

    class Config:
        from_attributes = True
        orm_mode = True

class MasterBrandRead(MasterBrandBase):
    id: int
    label: str
    created_at: datetime
    modified_at: datetime

class MasterBrandCreate(MasterBrandBase):
    pass