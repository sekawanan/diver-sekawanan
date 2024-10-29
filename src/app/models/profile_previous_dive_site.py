from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime

class ProfilePreviousDiveSite(Base):
    __tablename__ = "profile_previous_dive_sites"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    onboarding_profile_id = Column(Integer, ForeignKey("onboarding_profiles.id"), nullable=False)
    master_previous_dive_site_id = Column(Integer, ForeignKey("master_previous_dive_sites.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    onboarding_profile = relationship("OnboardingProfile", back_populates="profile_previous_dive_sites")
    master_previous_dive_site = relationship("MasterPreviousDiveSite", back_populates="profile_previous_dive_sites")
    # master_previous_dive_site = relationship("MasterPreviousDiveSite")
    @property
    def label(self):
        return self.master_previous_dive_site.label if self.master_previous_dive_site else None
