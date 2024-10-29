# app/models/profile_love_to.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime

class ProfileLoveTo(Base):
    __tablename__ = "profile_love_tos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    onboarding_profile_id = Column(Integer, ForeignKey("onboarding_profiles.id"), nullable=False)
    master_love_to_id = Column(Integer, ForeignKey("master_love_tos.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    onboarding_profile = relationship("OnboardingProfile", back_populates="profile_love_tos")
    master_love_to = relationship("MasterLoveTo", back_populates="profile_love_tos")
    # master_love_to = relationship("MasterLoveTo")
    @property
    def label(self):
        return self.master_love_to.label if self.master_love_to else None