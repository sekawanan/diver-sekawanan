# app/services/master_brand_service.py
from typing import List
from app.repositories.master_brand_repository import MasterBrandRepository
from app.models.master_brand import MasterBrand

class MasterBrandService:
    def __init__(self, repository: MasterBrandRepository):
        self.repository = repository
    
    async def get_all_master_brands(self) -> List[MasterBrand]:
        return await self.repository.get_all_master_brands()