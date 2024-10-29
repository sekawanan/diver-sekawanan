# app/services/master_gear_brand_service.py
from typing import List
from app.repositories.master_gear_brand_repository import MasterGearBrandRepository
from app.models.master_gear_brand import MasterGearBrand

class MasterGearBrandService():
    def __init__(self, repository: MasterGearBrandRepository):
        self.repository = repository
    
    async def get_all_master_gear_brands(self) -> List[MasterGearBrand]:
        return await self.repository.get_all_master_gear_brands()