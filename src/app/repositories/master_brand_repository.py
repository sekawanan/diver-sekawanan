# app/repositories/master_brand_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.master_brand import MasterBrand
from app.schemas.master_brand import MasterBrandCreate

class MasterBrandRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_master_brand_by_id(self, master_brand_id: int) -> MasterBrand:
        result = await self.db.execute(
            select(MasterBrand)
            .where(MasterBrand.id == master_brand_id))
        return result.scalar_one_or_none()
    
    async def get_all_master_brands(self) -> List[MasterBrand]:
        result = await self.db.execute(select(MasterBrand))
        brands = result.scalars().all()
        return brands
    
    async def create_master_brand(self, master_brand: MasterBrandCreate) -> List[MasterBrand]:
        master_brand_instance = MasterBrand(label=master_brand.label)
        self.db.add(master_brand_instance)
        await self.db.commit()
        await self.db.refresh(master_brand_instance)
        return master_brand_instance
    
    async def delete_master_brand(self, master_brand_id: int) -> List[MasterBrand]:
        result = await self.db.execute(select(MasterBrand).where(MasterBrand.id == master_brand_id))
        brand = result.scalar_one_or_none()
        if not brand:
            return False
        await self.db.delete(brand)
        await self.db.commit()
        return True