# app/repositories/master_color_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.master_color import MasterColor

class MasterColorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_master_color(self) -> List[MasterColor]:
        result = await self.db.execute(select(MasterColor))
        colors = result.scalars().all()
        return colors