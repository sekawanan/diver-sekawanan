from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict  # Import ConfigDict
from datetime import datetime

from .profile_previous_dive_site import ProfilePreviousDiveSiteRead


class MasterPreviousDiveSiteBase(BaseModel):
    label: Optional[str] = Field(None, max_length=255, description="Label of the master previous dive site")


class MasterPreviousDiveSiteCreate(MasterPreviousDiveSiteBase):
    pass  # Inherits all fields from Base


class MasterPreviousDiveSiteRead(MasterPreviousDiveSiteBase):
    id: int = Field(..., description="Unique identifier of the master previous dive site")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the record was created")
    modified_at: Optional[datetime] = Field(None, description="Timestamp when the record was last modified")

    model_config = ConfigDict(from_attributes=True)


class MasterPreviousDiveSiteWithProfiles(MasterPreviousDiveSiteRead):
    profile_previous_dive_sites: List[ProfilePreviousDiveSiteRead] = Field(default_factory=list, description="List of profile previous dive sites associated with this master site")

    model_config = ConfigDict(from_attributes=True)


# Update forward references
MasterPreviousDiveSiteWithProfiles.update_forward_refs()