# app/api/v1/endpoints/master_brand.py 
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.base_response import BaseResponse
from app.schemas.master_brand import MasterBrandCreate, MasterBrandRead
from app.services.master_brand_service import MasterBrandService
from app.repositories.master_brand_repository import MasterBrandRepository
from app.database.session import get_db
from app.utils.responses import create_error_response, create_success_response

api_router = APIRouter(
    prefix="/master-brands",
    tags=["Master Brand"],
    responses={404: {"description": "Not found"}},
)

@api_router.post("/", response_model=BaseResponse[List[MasterBrandRead]], status_code=status.HTTP_201_CREATED)
async def create_diver_gear(
    master_brand: MasterBrandCreate,
    db: AsyncSession = Depends(get_db),
):
    repository = MasterBrandRepository(db)
    service = MasterBrandService(repository)
    brands = await service.create_master_brand(master_brand)
    return create_success_response(brands)

@api_router.get("/", response_model=BaseResponse[List[MasterBrandRead]])
async def read_master_brands(db: AsyncSession = Depends(get_db)):
    repository = MasterBrandRepository(db)
    service = MasterBrandService(repository)
    brands = await service.get_all_master_brands()
    return create_success_response(brands)

@api_router.delete("/{master_brand_id}", response_model=BaseResponse[List[MasterBrandRead]])
async def read_master_brands(
    master_brand_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    repository = MasterBrandRepository(db)
    service = MasterBrandService(repository)
    is_success = await service.delete_master_brand(master_brand_id)
    if is_success :
        return create_success_response({"message": "Success Deleting Master Brand"})
    return create_error_response(message= "Fails Deleting Master Brand", code=400)