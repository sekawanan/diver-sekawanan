# app/repositories/diver_gear_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.diver_gear import DiverGear
from app.models.master_gear_brand import MasterGearBrand
from app.models.master_gear import MasterGear
from app.models.master_brand import MasterBrand
from app.schemas.diver_gear import DiverGearCreate

class DiverGearRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_gears_by_diver(self, diver_profile_id: int) -> List[DiverGear]:
        result = await self.db.execute(
            select(DiverGear)
            .options(
                selectinload(DiverGear.diver_profile),
                selectinload(DiverGear.master_brand),
            )
            .where(DiverGear.diver_profile_id == diver_profile_id)
        )

        diver_gears = result.scalars().all()
        return diver_gears
    
    async def create_gears_by_diver(self, diver_profile_id: int, diver_gear: DiverGearCreate, master_brand: MasterBrand) -> List[DiverGear]:
        diver_gear_instance = DiverGear(
            master_brand_id = master_brand.id,
            color = diver_gear.color,
            type = diver_gear.type
        )
        diver_gear_instance.diver_profile_id = diver_profile_id
        self.db.add(diver_gear_instance)
        await self.db.commit()
        await self.db.refresh(diver_gear_instance)
        
        result = await self.db.execute(
            select(DiverGear)
            .options(
                selectinload(DiverGear.diver_profile),
                selectinload(DiverGear.master_brand)
            )
            .where(DiverGear.diver_profile_id == diver_profile_id)
        )

        diver_gears = result.scalars().all()
        return diver_gears
    
    async def delete_gears_by_diver(self, diver_profile_id: int, diver_gear_id: int) -> List[DiverGear]:
        result = await self.db.execute(
            select(DiverGear)
            .options(
                selectinload(DiverGear.diver_profile),
                selectinload(DiverGear.master_brand),
            )
            .where(DiverGear.id == diver_gear_id & DiverGear.diver_profile_id == diver_profile_id)
        )

        diver_gear_instance = result.scalar_one_or_none()
        if not diver_gear_instance:
            return False
        await self.db.delete(diver_gear_instance)
        await self.db.commit()
        return True