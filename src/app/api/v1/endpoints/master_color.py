# app/api/v1/endpoints/master_color.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.master_color_repository import MasterColorRepository
from app.schemas.base_response import BaseResponse
from app.schemas.master_color import MasterColorRead
from app.services.master_color_service import MasterColorService
from app.database.session import get_db
from app.dependencies import get_master_color_service
from app.utils.responses import create_error_response, create_success_response

api_router = APIRouter(
    prefix="/master-colors",
    tags=["Master Color"],
    responses={404: {"description": "Not found"}},
)

@api_router.post("/", response_model=BaseResponse[List[MasterColorRead]], status_code=status.HTTP_201_CREATED)
async def create_diver_gear(
    master_color: MasterColorCreate,
    db: AsyncSession = Depends(get_db),
):
    repository = MasterColorRepository(db)
    service = MasterColorService(repository)
    brands = await service.create_master_color(master_color)
    return create_success_response(brands)

@api_router.get("/", response_model=BaseResponse[List[MasterColorRead]])
async def read_master_brands(db: AsyncSession = Depends(get_db)):
    repository = MasterColorRepository(db)
    service = MasterColorService(repository)
    brands = await service.get_all_master_colors()
    return create_success_response(brands)

@api_router.delete("/{master_color_id}", response_model=BaseResponse[List[MasterColorRead]])
async def read_master_brands(
    master_color_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    repository = MasterColorRepository(db)
    service = MasterColorService(repository)
    is_success = await service.delete_master_color(master_color_id)
    if is_success :
        return create_success_response({"message": "Success Deleting Master Color"})
    return create_error_response({"error": "Fails Deleting Master Color"})