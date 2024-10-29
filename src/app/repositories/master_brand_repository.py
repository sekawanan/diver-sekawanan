# app/repositories/master_brand_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.master_brand import MasterBrand

class MasterBrandRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_master_brands(self) -> List[MasterBrand]:
        result = await self.db.execute(select(MasterBrand))
        brands = result.scalars().all()
        return brands