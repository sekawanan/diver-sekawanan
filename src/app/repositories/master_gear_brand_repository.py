# app/repositories/master_gear_brand_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.master_gear_brand import MasterGearBrand

class MasterGearBrandRepository():
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_master_gear_brands(self) -> List[MasterGearBrand]:
        result = await self.db.execute(
            select(MasterGearBrand)
            .options(selectinload(MasterGearBrand.master_brands))
            .options(selectinload(MasterGearBrand.master_gears))
            )
        gear_brands = result.scalars().all()
        return gear_brands