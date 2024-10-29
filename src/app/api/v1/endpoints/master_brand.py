# app/api/v1/endpoints/master_brand.py 
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.master_brand import MasterBrandRead
from app.services.master_brand_service import MasterBrandService
from app.repositories.master_brand_repository import MasterBrandRepository
from app.database.session import get_db

api_router = APIRouter()

@api_router.get("/", response_model=List[MasterBrandRead])
async def read_master_brands(db: AsyncSession = Depends(get_db)):
    repository = MasterBrandRepository(db)
    service = MasterBrandService(repository)
    brands = await service.get_all_master_brands()
    return brands