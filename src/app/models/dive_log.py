# app/models/dive_logs.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Time,
    SmallInteger,
    DECIMAL,
)
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime
import enum

class DiveSuitEnum(enum.Enum):
    DRY_SUIT = "Dry Suit"
    WET_SUIT = "Wet Suit"
    OTHER = "Other"

class DiveLog(Base):
    __tablename__ = "dive_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    diver_profile_id = Column(Integer, ForeignKey("diver_profiles.id"), nullable=False)
    master_dive_site_id = Column(Integer, ForeignKey("master_dive_sites.id"), nullable=False)
    master_dive_type_id = Column(Integer, ForeignKey("master_dive_types.id"), nullable=False)
    dive_suit = Column(Enum(DiveSuitEnum), nullable = True)
    dive_log_date = Column(DateTime, nullable=False)
    time_in = Column(Time, nullable=True)
    time_out = Column(Time, nullable=True)
    max_depth = Column(SmallInteger, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    #Relationships
    diver_profile = relationship("DiverProfile", back_populates="dive_logs")
    master_dive_site = relationship("MasterDiveSite", back_populates="dive_logs")
    master_dive_type = relationship("MasterDiveType", back_populates="dive_logs")