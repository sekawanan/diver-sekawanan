# app/schemas/onboarding_profile.py

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime

from .profile_previous_dive_site import ProfilePreviousDiveSiteRead
from .profile_love_to import ProfileLoveToRead
from app.models.enums import (
    GenderEnum,
    CertificationEnum,
    CertificationIssuerEnum,
    WantToSeeEnum,
    DiveConditionEnum,
    BottomTimeEnum,
    TroubleEqualizingEnum,
)

class OnboardingProfileBase(BaseModel):
    gender: Optional[GenderEnum] = Field(None, description="Gender of the user")
    start_diving: Optional[date] = Field(None, description="Start date of diving")
    last_time_diving: Optional[date] = Field(None, description="Last time the user dived")
    current_logs: Optional[int] = Field(None, description="Current logs of diving")
    last_certification: Optional[CertificationEnum] = Field(None, description="Last certification achieved")
    certification_issuer: Optional[CertificationIssuerEnum] = Field(None, description="Issuer of the certification")
    want_to_see: Optional[WantToSeeEnum] = Field(None, description="Things the user wants to see while diving")
    dive_current_condition: Optional[DiveConditionEnum] = Field(None, description="User's current condition while diving")
    bottom_time: Optional[BottomTimeEnum] = Field(None, description="Bottom time preferences")
    trouble_equalizing: Optional[TroubleEqualizingEnum] = Field(None, description="Trouble equalizing frequency")
    photographer: Optional[bool] = Field(None, description="Is the user a photographer?")
    information: Optional[str] = Field(None, description="Additional information")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the record was created")
    modified_at: Optional[datetime] = Field(None, description="Timestamp when the record was last modified")

class OnboardingProfileCreate(OnboardingProfileBase):
    pass  # Inherits all fields from Base

class OnboardingProfileCreateRequest(BaseModel):
    gender: GenderEnum
    start_diving: date
    last_time_diving: date
    current_logs: int
    last_certification: CertificationEnum
    certification_issuer: CertificationIssuerEnum
    want_to_see: WantToSeeEnum
    dive_current_condition: DiveConditionEnum
    bottom_time: BottomTimeEnum
    trouble_equalizing: TroubleEqualizingEnum
    photographer: bool
    information: Optional[str] = None
    master_love_to_ids: List[int] = Field(
        default_factory=list,
        description="List of Master Love To IDs to associate"
    )
    master_previous_dive_site_ids: List[int] = Field(
        default_factory=list,
        description="List of Master Previous Dive Site IDs to associate"
    )

class OnboardingProfileUpdate(OnboardingProfileBase):
    gender: GenderEnum
    start_diving: date
    last_time_diving: date
    current_logs: int
    last_certification: CertificationEnum
    certification_issuer: CertificationIssuerEnum
    want_to_see: WantToSeeEnum
    dive_current_condition: DiveConditionEnum
    bottom_time: BottomTimeEnum
    trouble_equalizing: TroubleEqualizingEnum
    photographer: bool
    information: Optional[str] = None
    master_love_to_ids: List[int] = Field(
        default_factory=list,
        description="List of Master Love To IDs to associate"
    )
    master_previous_dive_site_ids: List[int] = Field(
        default_factory=list,
        description="List of Master Previous Dive Site IDs to associate"
    )

    model_config = ConfigDict(from_attributes=True)
    
class OnboardingProfileRead(OnboardingProfileBase):
    id: int = Field(..., description="Unique identifier of the onboarding profile")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the profile was created")
    modified_at: Optional[datetime] = Field(None, description="Timestamp when the profile was last modified")

    model_config = ConfigDict(from_attributes=True)

class OnboardingProfileWithRelations(OnboardingProfileRead):
    profile_previous_dive_sites: List[ProfilePreviousDiveSiteRead] = Field(
        default_factory=list, 
        description="List of previous dive sites associated with the profile"
    )
    profile_love_tos: List[ProfileLoveToRead] = Field(
        default_factory=list, 
        description="List of love to entries associated with the profile"
    )

    model_config = ConfigDict(from_attributes=True)

# Update forward references if necessary
OnboardingProfileWithRelations.update_forward_refs()