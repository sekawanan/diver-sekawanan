# app/schemas/master_dive_type.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MasterDiveTypeBase(BaseModel):
    label:str

class MasterDiveTypeCreate(MasterDiveTypeBase):

    pass

class MasterDiveTypeUpdate(MasterDiveTypeBase):

    pass

class MasterDiveTypeRead(MasterDiveTypeBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True