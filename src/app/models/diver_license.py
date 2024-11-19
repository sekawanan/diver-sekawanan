# app/models/diver_license.py
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, DateTime, Date
from app.database.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class DiverLicense(Base):
    __tablename__ = "diver_licenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    diver_profile_id = Column(Integer, ForeignKey("diver_profiles.id", ondelete="CASCADE"), nullable=False)
    license_institution = Column(String(100), nullable=False)
    license_level = Column(String(100), nullable=False)
    diver_name = Column(String(100), nullable=False)
    diver_number = Column(String(100), nullable=False)
    birth_date_license = Column(Date, nullable=True)
    certificate_date = Column(Date, nullable=True)
    instructor_name = Column(String(100), nullable=True)
    instructor_number = Column(String(100), nullable=True)
    store_name = Column(String(100), nullable=True)
    store_number = Column(Integer, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    diver_profile = relationship("DiverProfile", back_populates="diver_licenses")