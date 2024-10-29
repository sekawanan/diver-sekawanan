# app/models/master_license.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime

class MasterLicense(Base):
    __tablename__ = "master_licenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    title = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    issuer = Column(String(50), nullable=False)
    alias = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# Define the relationship
    diver_licenses = relationship("DiverLicense", back_populates="master_license")