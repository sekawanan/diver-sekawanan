from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict  # Import ConfigDict
from datetime import date, datetime


class ProfileLoveToBase(BaseModel):
    onboarding_profile_id: Optional[int] = Field(None, description="ID of the onboarding profile")
    master_love_to_id: Optional[int] = Field(None, description="ID of the master love to")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the record was created")
    modified_at: Optional[datetime] = Field(None, description="Timestamp when the record was last modified")


class ProfileLoveToCreate(ProfileLoveToBase):
    pass  # Inherits all fields from Base


class ProfileLoveToUpdate(ProfileLoveToBase):
    onboarding_profile_id: Optional[int] = Field(None, description="Updated onboarding profile ID")
    master_love_to_id: Optional[int] = Field(None, description="Updated master love to ID")

    model_config = ConfigDict(from_attributes=True)


class ProfileLoveToRead(ProfileLoveToBase):
    id: int = Field(..., description="Unique identifier of the profile love to")
    label: str = Field(..., description="Label of the love to")

    model_config = ConfigDict(from_attributes=True)