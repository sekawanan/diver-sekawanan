# app/services/diver_gear_service.py
from typing import List, Optional
from app.models.diver_gear import DiverGear
from app.schemas.diver_gear import DiverGearCreate, DiverGearUpdate
from app.repositories.diver_gear_repository import DiverGearRepository

class DiverGearService:
    def __init__(self, repository: DiverGearRepository):
        self.repository = repository
    
    # async def get_all_diver_gear(self) -> List[DiverGear]:
    #     return await self.repository.get_gears_by_diver

    async def get_gears_by_diver(self, diver_profile_id: int) -> List[DiverGear]:
        return await self.repository.get_gears_by_diver(diver_profile_id)