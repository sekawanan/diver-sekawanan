# app/api/v1/endpoints/master_dive_preference.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.master_dive_preference import MasterDivePreferenceRead, MasterDivePreferenceCreate
from app.database.session import get_db
from app.repositories.master_dive_preference_repository import MasterDivePreferenceRepository
from app.services.master_dive_preference_service import MasterDivePreferenceService

api_router = APIRouter()

@api_router.post("/master-dive-preferences", response_model=MasterDivePreferenceRead, status_code=status.HTTP_201_CREATED)
async def create_master_dive_preference(
    preference: MasterDivePreferenceCreate,
    db: AsyncSession = Depends(get_db)
):
    repository = MasterDivePreferenceRepository(db)
    service = MasterDivePreferenceService(repository)
    new_preference = MasterDivePreferenceRead(**preference.dict())
    created_preference = await service.create_master_dive_preference(new_preference)
    return created_preference

@api_router.get("/master-dive-preferences", response_model=List[MasterDivePreferenceRead])
async def get_master_dive_preferences(
    db: AsyncSession = Depends(get_db)
):
    repository = MasterDivePreferenceRepository(db)
    service = MasterDivePreferenceService(repository)
    preferences = await service.get_all_master_dive_preferences()
    return preferences