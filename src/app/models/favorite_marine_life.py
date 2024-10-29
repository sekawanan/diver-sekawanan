# app/models/favorite_marine_life.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from app.database.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class FavoriteMarineLife(Base):
    __tablename__ = "favorite_marine_lifes"
    __table_args__ = (
        UniqueConstraint('diver_profile_id', 'master_marine_life_id', name='uix_diver_master_favorite_marine_life'),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    diver_profile_id = Column(Integer, ForeignKey("diver_profiles.id"), nullable=False)
    master_marine_life_id = Column(Integer, ForeignKey("master_marine_lifes.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    diver_profile = relationship("DiverProfile", back_populates="favorite_marine_lifes")
    master_marine_life = relationship("MasterMarineLife", back_populates="favorite_marine_lifes")