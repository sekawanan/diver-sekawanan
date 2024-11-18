# app/models/diver_profile.py
from sqlalchemy import Column, Integer, String, DateTime, Date
from app.database.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class DiverProfile(Base):
    __tablename__ = "diver_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    user_id = Column(String(36), index=True, nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    full_name = Column(String(100), nullable=False)
    profile_picture_url = Column(String(), nullable=True)
    birth_date = Column(Date, default=datetime(1970, 1, 1), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    diver_additional_data = relationship("DiverAdditionalData", back_populates="diver_profile")
    diver_licenses = relationship("DiverLicense", back_populates="diver_profile")
    dive_preferences = relationship("DivePreference", back_populates="diver_profile")
    diver_gears = relationship("DiverGear", back_populates="diver_profile")
    dive_logs = relationship("DiveLog", back_populates="diver_profile")
    favorite_marine_lifes = relationship("FavoriteMarineLife", back_populates="diver_profile")