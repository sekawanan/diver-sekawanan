# app/api/v1/endpoints/master_license.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.master_license import MasterLicenseRead
from app.services.master_license_service import MasterLicenseService
from app.repositories.master_license_repository import MasterLicenseRepository
from app.database.session import get_db

api_router = APIRouter()

@api_router.get("/master-licenses", response_model=List[MasterLicenseRead])
async def read_master_licenses(db: AsyncSession = Depends(get_db)):
    repository = MasterLicenseRepository(db)
    service = MasterLicenseService(repository)
    licenses = await service.get_all_master_licenses()
    return licenses

@api_router.get("/master-licenses/{master_license_id}", response_model=MasterLicenseRead)
async def read_master_license(master_license_id: int, db: AsyncSession = Depends(get_db)):
    repository = MasterLicenseRepository(db)
    service = MasterLicenseService(repository)
    license = await service.get_master_license(master_license_id)
    if not license:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Master license not found")
    return license