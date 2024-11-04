# app/models/diver_gear.py
from typing import List, Optional
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from app.database.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class DiverGear(Base):
    __tablename__ = "diver_gears"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    diver_profile_id = Column(Integer, ForeignKey("diver_profiles.id"), nullable=False)
    master_gears_brand_id = Column(Integer, ForeignKey("master_gears_brands.id"), nullable=False)
    master_color_id = Column(Integer, ForeignKey("master_colors.id"), nullable=False)
    type = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    diver_profile = relationship("DiverProfile", back_populates="diver_gears")
    master_gears_brand = relationship("MasterGearBrand", back_populates="diver_gears")
    master_color = relationship("MasterColor", back_populates="diver_gears")

    # Define properties to flatten nested relationships
    @property
    def color_label(self) -> Optional[str]:
        return self.master_color.color_label if self.master_color else None

    @property
    def gear_label(self) -> Optional[str]:
        return self.master_gears_brand.master_gear.label if self.master_gears_brand and self.master_gears_brand.master_gear else None

    @property
    def brand_label(self) -> Optional[str]:
        return self.master_gears_brand.master_brand.label if self.master_gears_brand and self.master_gears_brand.master_brand else None