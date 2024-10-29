# app/models/onboarding_profile.py
from sqlalchemy import Column, Integer, Enum, Date, Boolean, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime
from .enums import (
    GenderEnum,
    CertificationEnum,
    CertificationIssuerEnum,
    WantToSeeEnum,
    DiveConditionEnum,
    BottomTimeEnum,
    TroubleEqualizingEnum,
)

class OnboardingProfile(Base):
    __tablename__ = "onboarding_profiles"
    __table_args__ = (
        UniqueConstraint('user_id', name='uq_onboarding_profiles_user_id'),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    start_diving = Column(Date, nullable=True)
    last_time_diving = Column(Date, nullable=True)
    current_logs = Column(Integer, nullable=True)
    last_certification = Column(Enum(CertificationEnum), nullable=True)
    certification_issuer = Column(Enum(CertificationIssuerEnum), nullable=True)
    want_to_see = Column(Enum(WantToSeeEnum), nullable=True)
    dive_current_condition = Column(Enum(DiveConditionEnum), nullable=True)
    bottom_time = Column(Enum(BottomTimeEnum), nullable=True)
    trouble_equalizing = Column(Enum(TroubleEqualizingEnum), nullable=True)
    photographer = Column(Boolean, nullable=True)
    information = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="onboarding_profiles")
    profile_love_tos = relationship(
        "ProfileLoveTo",
        back_populates="onboarding_profile",
        cascade="all, delete-orphan",
        lazy="selectin"  # Efficient eager loading
    )
    profile_previous_dive_sites = relationship(
        "ProfilePreviousDiveSite",
        back_populates="onboarding_profile",
        cascade="all, delete-orphan",
        lazy="selectin"  # Efficient eager loading
    )