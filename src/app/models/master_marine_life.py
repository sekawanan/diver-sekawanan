# app/models/master_marine_life.py
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class MasterMarineLife(Base):
    __tablename__ = "master_marine_lifes"

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    label = Column(String(100), nullable=False)
    image_url = Column(String(1000), nullable=False)
    image_credit = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # master_gear_brands = relationship("MasterGearBrand", back_populates="master_color")
    favorite_marine_lifes = relationship("FavoriteMarineLife", back_populates="master_marine_life")