# app/repositories/master_marine_life_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.master_marine_life import MasterMarineLife

class MasterMarineLifeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_master_marine_life(self) -> List[MasterMarineLife]:
        result = await self.db.execute(select(MasterMarineLife))
        marine_life = result.scalars().all()
        return marine_life