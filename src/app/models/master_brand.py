# app/models/master_brand.py
from sqlalchemy import Column, Integer, String, DateTime
from app.database.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class MasterBrand(Base):
    __tablename__ = "master_brands"

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    label = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    diver_gears = relationship("DiverGear", back_populates="master_brand")