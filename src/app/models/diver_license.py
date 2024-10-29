# app/models/diver_license.py
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Date
from app.database.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class DiverLicense(Base):
    __tablename__ = "diver_licenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    diver_profile_id = Column(Integer, ForeignKey("diver_profiles.id", ondelete="CASCADE"), nullable=False)
    master_license_id = Column(Integer, ForeignKey("master_licenses.id", ondelete="RESTRICT"), nullable=False)
    certification_number = Column(String(100), nullable=False)
    certificate_date = Column(Date, nullable=True)
    birth_date_license = Column(Date, nullable=True)
    instructor_name = Column(String(100), nullable=True)
    instructor_number = Column(Integer, nullable=True)
    store_name = Column(String(100), nullable=True)
    store_number = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    diver_profile = relationship("DiverProfile", back_populates="diver_licenses")
    master_license = relationship("MasterLicense", back_populates="diver_licenses")