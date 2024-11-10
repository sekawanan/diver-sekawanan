# app/services/diver_gear_service.py
from typing import List, Optional

from fastapi import HTTPException, logger
from app.models.diver_gear import DiverGear
from app.repositories.master_brand_repository import MasterBrandRepository
from app.schemas.diver_gear import DiverGearCreate, DiverGearRead, DiverGearUpdate
from app.repositories.diver_gear_repository import DiverGearRepository

class DiverGearService:
    def __init__(
            self,
            diver_gear_repository: DiverGearRepository,
            master_brand_repository: MasterBrandRepository
        ):
        self.diver_gear_repository = diver_gear_repository
        self.master_brand_repository = master_brand_repository

    async def get_gears_by_diver(self, diver_profile_id: int) -> List[DiverGear]:
        fetched_gears = await self.diver_gear_repository.get_gears_by_diver(diver_profile_id)
        return [DiverGearRead.from_orm(gear) for gear in fetched_gears]
    
    async def create_gears_by_diver(self, diver_profile_id: int, diver_gear: DiverGearCreate) -> List[DiverGear]:
        master_brand = await self.master_brand_repository.get_master_brand_by_id(diver_gear.master_brand_id)
        diver_gears = await self.diver_gear_repository.create_gears_by_diver(diver_profile_id, diver_gear, master_brand)
        return [DiverGearRead.from_orm(gear) for gear in diver_gears]
    
    async def delete_gears_by_diver(self, diver_profile_id: int, diver_gear_id: int) -> List[DiverGear]:
        return await self.repository.delete_gears_by_diver(diver_profile_id, diver_gear_id)