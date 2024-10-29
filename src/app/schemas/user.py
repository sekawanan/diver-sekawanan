# app/schemas/user.py
from __future__ import annotations  # For forward references
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict  # Import ConfigDict
from datetime import datetime

from .onboarding_profile import OnboardingProfileRead  # Import forward reference


class UserBase(BaseModel):
    username: str = Field(..., max_length=255, description="Unique username of the user")
    full_name: Optional[str] = Field(None, max_length=255, description="Full name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    is_active: bool = Field(True, description="Indicates if the user is active")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password for the user account")


class UserRead(UserBase):
    id: int = Field(..., description="Unique identifier of the user")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the user was created")
    modified_at: Optional[datetime] = Field(None, description="Timestamp when the user was last modified")

    model_config = ConfigDict(from_attributes=True)

# app/schemas/user.py

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=255)
    full_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    # Add other fields as necessary
    
    model_config = ConfigDict(from_attributes=True)

class UserWithProfiles(UserRead):
    onboarding_profiles: List[OnboardingProfileRead] = Field(default_factory=list, description="List of onboarding profiles associated with the user")

    model_config = ConfigDict(from_attributes=True)

# Pydantic model for input
class TokenInput(BaseModel):
    token: str

    class Config:
        from_attributes = True

# Update forward references
UserWithProfiles.update_forward_refs()

