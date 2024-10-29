# app/api/v1/endpoints/master_dive_site.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.master_dive_site import MasterDiveSiteRead
from app.services.master_dive_site_service import MasterDiveSiteService
from app.repositories.master_dive_site_repository import MasterDiveSiteRepository
from app.database.session import get_db

api_router = APIRouter()

@api_router.get("/master-dive_sites", response_model=List[MasterDiveSiteRead])
async def read_master_colors(db: AsyncSession = Depends(get_db)):
    repository = MasterDiveSiteRepository(db)
    service = MasterDiveSiteService(repository)
    dive_sites = await service.get_all_master_dive_sites()
    return dive_sites