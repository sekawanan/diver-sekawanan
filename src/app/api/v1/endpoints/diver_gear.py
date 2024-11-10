# app/api/v1/endpoints/diver_gear.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user_id
from app.dependencies import get_diver_profile_service
from app.repositories.master_brand_repository import MasterBrandRepository
from app.repositories.master_gear_repository import MasterGearRepository
from app.schemas.base_response import BaseResponse
from app.schemas.diver_gear import DiverGearCreate, DiverGearUpdate, DiverGearRead
from app.services.diver_gear_service import DiverGearService
from app.repositories.diver_gear_repository import DiverGearRepository
from app.database.session import get_db
from app.services.diver_profile_service import DiverProfileService
from app.services.master_brand_service import MasterBrandService
from app.utils.responses import create_success_response

api_router = APIRouter(
    prefix="/diver-gears",
    tags=["Diver Gear"],
    responses={404: {"description": "Not found"}},
)

@api_router.post("/me", response_model=BaseResponse[List[DiverGearRead]], status_code=status.HTTP_201_CREATED)
async def create_diver_gear(
    diver_gear_create: DiverGearCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
    profileService: DiverProfileService = Depends(get_diver_profile_service)
):
    print(user_id)
    repository = DiverGearRepository(db)
    master_brand_repository = MasterBrandRepository(db)
    service = DiverGearService(repository, master_brand_repository)
    profile = await profileService.get_diver_profile(user_id)
    diver_gears = await service.create_gears_by_diver(profile.id, diver_gear_create)
    
    return create_success_response(diver_gears)

@api_router.get("/me", response_model=BaseResponse[List[DiverGearRead]])
async def read_diver_gear(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
    profileService: DiverProfileService = Depends(get_diver_profile_service)
):
    repository = DiverGearRepository(db)
    brand_repository = MasterBrandRepository(db)
    service = DiverGearService(repository, brand_repository)
    brand_service = MasterBrandService(brand_repository)
    profile = await profileService.get_diver_profile(user_id)
    diver_gears = await service.get_gears_by_diver(profile.id)
    for diver_gear in diver_gears:
        master_brand =await brand_service.get_master_brand_by_id(diver_gear.master_brand_id)
        diver_gear.brand_label = master_brand.label

    return create_success_response(diver_gears)

@api_router.delete("/me/{diver_gear_id}", response_model=BaseResponse[List[DiverGearRead]])
async def read_diver_gear(
    diver_gear_id: int,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
    profileService: DiverProfileService = Depends(get_diver_profile_service)
):
    repository = DiverGearRepository(db)
    brand_repository = MasterBrandRepository(db)
    service = DiverGearService(repository, brand_repository)
    profile = await profileService.get_diver_profile(user_id)
    diver_gears = await service.delete_gears_by_diver(profile.id, diver_gear_id)

    return create_success_response({"message": "Success delete diver_gear"})