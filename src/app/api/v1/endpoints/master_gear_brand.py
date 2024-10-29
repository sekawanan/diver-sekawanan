# app/api/v1/endpoints/master_gear_brand.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.master_gear_brand import MasterGearBrandRead
from app.services.master_gear_brand_service import MasterGearBrandService
from app.repositories.master_gear_brand_repository import MasterGearBrandRepository
from app.database.session import get_db

api_router = APIRouter()

@api_router.get("/master-gears-brands", response_model=List[MasterGearBrandRead])
async def read_master_gears_brands(db: AsyncSession = Depends(get_db)):
    repository = MasterGearBrandRepository(db)
    service = MasterGearBrandService(repository)
    gear_brands = await service.get_all_master_gear_brands()
    
    for gear_brand in gear_brands:
        gear_brand.gear_label = gear_brand.master_gears.label
        gear_brand.brand_label = gear_brand.master_brands.label
        
    return gear_brands