# app/repositories/master_gear_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.master_gear import MasterGear

class MasterGearRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_master_gears(self) -> List[MasterGear]:
        result = await self.db.execute(select(MasterGear))
        gears = result.scalars().all()
        return gears
