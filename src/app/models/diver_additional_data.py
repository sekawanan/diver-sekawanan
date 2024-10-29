# app/models/diver_additional_data.py
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from app.database.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class DiverAdditionalData(Base):
    __tablename__ = "diver_additional_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    diver_profile_id = Column(Integer, ForeignKey("diver_profiles.id"), nullable=False)
    total_dive_log = Column(Integer, default=0, nullable=False)
    total_visited_dive_site = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    diver_profile = relationship("DiverProfile", back_populates="diver_additional_data")