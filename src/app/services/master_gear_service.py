# app/services/master_gear_service.py
from typing import List
from app.repositories.master_gear_repository import MasterGearRepository
from app.models.master_gear import MasterGear

class MasterGearService:
    def __init__(self, repository: MasterGearRepository):
        self.repository = repository
    
    async def get_all_master_gears(self) -> List[MasterGear]:
        return await self.repository.get_all_master_gears()

