from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict  # Import ConfigDict
from datetime import datetime


class ProfilePreviousDiveSiteBase(BaseModel):
    onboarding_profile_id: Optional[int] = Field(None, description="ID of the onboarding profile")
    master_previous_dive_site_id: Optional[int] = Field(None, description="ID of the master previous dive site")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the record was created")
    modified_at: Optional[datetime] = Field(None, description="Timestamp when the record was last modified")


class ProfilePreviousDiveSiteCreate(ProfilePreviousDiveSiteBase):
    pass  # Inherits all fields from Base


class ProfilePreviousDiveSiteUpdate(ProfilePreviousDiveSiteBase):
    onboarding_profile_id: Optional[int] = Field(None, description="Updated onboarding profile ID")
    master_previous_dive_site_id: Optional[int] = Field(None, description="Updated master previous dive site ID")

    model_config = ConfigDict(from_attributes=True)


class ProfilePreviousDiveSiteRead(ProfilePreviousDiveSiteBase):
    id: int = Field(..., description="Unique identifier of the profile previous dive site")
    label: Optional[str] = Field(None, description="Label of the previous dive site")

    model_config = ConfigDict(from_attributes=True)