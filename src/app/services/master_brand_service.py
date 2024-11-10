# app/services/master_brand_service.py
from typing import List
from app.repositories.master_brand_repository import MasterBrandRepository
from app.models.master_brand import MasterBrand
from app.schemas.master_brand import MasterBrandCreate, MasterBrandRead

class MasterBrandService:
    def __init__(self, repository: MasterBrandRepository):
        self.repository = repository
    
    async def get_all_master_brands(self) -> List[MasterBrand]:
        fetched_brands = await self.repository.get_all_master_brands()
        return [MasterBrandRead.from_orm(brand) for brand in fetched_brands]
    
    async def get_master_brand_by_id(self, master_brand_id: int) -> MasterBrand:
        fetched_brand = await self.repository.get_master_brand_by_id(master_brand_id)
        return MasterBrandRead.from_orm(fetched_brand)

    async def create_master_brand(self, master_brand: MasterBrandCreate) -> List[MasterBrand]:
        created_brand = await self.repository.create_master_brand(master_brand)
        return MasterBrandRead.from_orm(created_brand)
    
    async def delete_master_brand(self, master_brand_id: int) -> List[MasterBrand]:
        return await self.repository.delete_master_brand(master_brand_id)