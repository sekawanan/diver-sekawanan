from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class MasterPreviousDiveSite(Base):
    __tablename__ = "master_previous_dive_sites"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    label = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile_previous_dive_sites = relationship("ProfilePreviousDiveSite", back_populates="master_previous_dive_site")
