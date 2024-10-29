# app/models/master_gear_brand.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class MasterGearBrand(Base):
    __tablename__ = "master_gears_brands"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    master_gear_id = Column(Integer, ForeignKey("master_gears.id"), nullable=False)
    master_brand_id = Column(Integer, ForeignKey("master_brands.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    diver_gears = relationship("DiverGear", back_populates="master_gears_brand")
    master_gear = relationship("MasterGear", back_populates="master_gears_brands")
    master_brand = relationship("MasterBrand", back_populates="master_gears_brands")