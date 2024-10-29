# app/schemas/favorite_marine_life.py

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

# Import the referenced schema
from .master_marine_life import MasterMarineLifeRead

class FavoriteMarineLifeRead(BaseModel):
    id: int
    diver_profile_id: int
    master_marine_life_id: int
    master_marine_life: MasterMarineLifeRead
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True

class FavoriteMarineLifeCreate(BaseModel):
    master_marine_life_id: int

    @validator('master_marine_life_id')
    def id_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('master_marine_life_id must be a positive integer')
        return v

class FavoriteMarineLifeCreateMultiple(BaseModel):
    master_marine_life_ids: List[int]

    @validator('master_marine_life_ids')
    def ids_must_be_positive(cls, v):
        if not all(id > 0 for id in v):
            raise ValueError('All master_marine_life_ids must be positive integers')
        if len(v) != len(set(v)):
            raise ValueError('master_marine_life_ids must be unique')
        return v

class FavoriteMarineLifeUpdate(BaseModel):
    master_marine_life_id: Optional[int] = None

    @validator('master_marine_life_id')
    def id_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('master_marine_life_id must be a positive integer')
        return v