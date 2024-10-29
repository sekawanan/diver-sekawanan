# app/models/master_dive_preference.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime

class MasterDivePreference(Base):
    __tablename__ = "master_dive_preferences"

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    label = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    dive_preferences = relationship("DivePreference", back_populates="master_preference")