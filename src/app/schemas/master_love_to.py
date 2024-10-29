from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict  # Import ConfigDict
from datetime import datetime

from .profile_love_to import ProfileLoveToRead


class MasterLoveToBase(BaseModel):
    label: Optional[str] = Field(None, max_length=255, description="Label of the master love to")


class MasterLoveToCreate(MasterLoveToBase):
    pass  # Inherits all fields from Base

class MasterLoveToUpdate(MasterLoveToBase):
    label: Optional[str] = Field(None, max_length=255, description="Updated label of the master love to")

    model_config = ConfigDict(from_attributes=True)

class MasterLoveToRead(MasterLoveToBase):
    id: int = Field(..., description="Unique identifier of the master love to")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the record was created")
    modified_at: Optional[datetime] = Field(None, description="Timestamp when the record was last modified")

    model_config = ConfigDict(from_attributes=True)


class MasterLoveToWithProfiles(MasterLoveToRead):
    profile_love_tos: List[ProfileLoveToRead] = Field(default_factory=list, description="List of profile love tos associated with this master love to")

    model_config = ConfigDict(from_attributes=True)


# Update forward references
MasterLoveToWithProfiles.update_forward_refs()