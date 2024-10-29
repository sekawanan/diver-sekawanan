# app/models/master_dive_type.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime
from app.database.session import Base
from datetime import datetime

class MasterDiveType(Base):
    __tablename__ = "master_dive_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    label = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    #Relationship
    dive_logs = relationship("DiveLog", back_populates="master_dive_type")