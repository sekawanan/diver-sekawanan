# app/repositories/master_dive_site_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.master_dive_site import MasterDiveSite

class MasterDiveSiteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_master_dive_site(self) -> List[MasterDiveSite]:
        result = await self.db.execute(select(MasterDiveSite))
        master_dive_site = result.scalars().all()
        return master_dive_site