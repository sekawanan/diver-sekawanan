# app/models/master_dive_site.py
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from app.database.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class MasterDiveSite(Base):
    __tablename__ = "master_dive_sites"

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    label = Column(String(100), nullable=False)
    latitude = Column(DECIMAL(10,8), nullable=False)
    longitude = Column(DECIMAL(11,8), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    dive_logs = relationship("DiveLog", back_populates="master_dive_site")
    # master_gear_brands = relationship("MasterGearBrand", back_populates="master_color")
    # diver_gears = relationship("DiverGear", back_populates="master_colors")