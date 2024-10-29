from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class MasterLoveTo(Base):
    __tablename__ = "master_love_tos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    label = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile_love_tos = relationship("ProfileLoveTo", back_populates="master_love_to")
