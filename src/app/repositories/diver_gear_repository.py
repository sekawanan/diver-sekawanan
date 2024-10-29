# app/repositories/diver_gear_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.diver_gear import DiverGear
from app.models.master_gear_brand import MasterGearBrand
from app.models.master_gear import MasterGear
from app.models.master_brand import MasterBrand

class DiverGearRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_gears_by_diver(self, diver_profile_id: int) -> List[DiverGear]:
        result = await self.db.execute(
            select(DiverGear)
            .options(
                selectinload(DiverGear.diver_profile),
                selectinload(DiverGear.master_gears_brand)
                    .selectinload(MasterGearBrand.master_gear),
                selectinload(DiverGear.master_gears_brand)
                    .selectinload(MasterGearBrand.master_brand),
                selectinload(DiverGear.master_colors),
            )
            .where(DiverGear.diver_profile_id == diver_profile_id)
        )

        diver_gears = result.scalars().all()
        return diver_gears