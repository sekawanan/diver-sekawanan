# app/repositories/master_dive_preference_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.master_dive_preference import MasterDivePreference

class MasterDivePreferenceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_master_dive_preferences(self) -> List[MasterDivePreference]:
        result = await self.db.execute(select(MasterDivePreference))
        preferences = result.scalars().all()
        return preferences

    async def create_master_dive_preference(self, preference: MasterDivePreference) -> MasterDivePreference:
        self.db.add(preference)
        await self.db.commit()
        await self.db.refresh(preference)
        return preference