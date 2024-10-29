# app/api/v1/endpoints/diver_gear.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.diver_gear import DiverGearCreate, DiverGearUpdate, DiverGearRead
from app.services.diver_gear_service import DiverGearService
from app.repositories.diver_gear_repository import DiverGearRepository
from app.database.session import get_db

api_router = APIRouter()

@api_router.get("/diver-gears/{diver_profile_id}", response_model=List[DiverGearRead])
async def read_diver_gear(
    diver_profile_id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = DiverGearRepository(db)
    service = DiverGearService(repository)
    diver_gears = await service.get_gears_by_diver(diver_profile_id)
    
    # Manually set the labels if needed
    for diver_gear in diver_gears:
        diver_gear.gear_label = diver_gear.master_gears_brand.master_gear.label
        diver_gear.brand_label = diver_gear.master_gears_brand.master_brand.label
        diver_gear.color_label = diver_gear.master_color.label

    return diver_gears
