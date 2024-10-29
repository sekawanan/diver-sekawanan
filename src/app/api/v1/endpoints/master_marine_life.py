# app/api/v1/endpoints/master_marine_life.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.master_marine_life import MasterMarineLifeRead
from app.repositories.master_marine_life_repository import MasterMarineLifeRepository
from app.services.master_marine_life_service import MasterMarineLifeService
from app.database.session import get_db

api_router = APIRouter()

@api_router.get("/master-marine-lifes", response_model=List[MasterMarineLifeRead])
async def read_master_marine_lifes(db: AsyncSession = Depends(get_db)):
    repository = MasterMarineLifeRepository(db)
    service = MasterMarineLifeService(repository)
    marine_lifes = await service.get_all_master_marine_lifes()
    return marine_lifes