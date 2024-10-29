from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.master_dive_type import MasterDiveTypeRead, MasterDiveTypeCreate, MasterDiveTypeUpdate
from app.services.master_dive_type_service import MasterDiveTypeService
from app.repositories.master_dive_type_repository import MasterDiveTypeRepository
from app.database.session import get_db

api_router = APIRouter()

# Dependency Injection to create DiveTypeService instance
def get_dive_type_service(db: AsyncSession = Depends(get_db)) -> MasterDiveTypeService:
    repository = MasterDiveTypeRepository(db)
    return MasterDiveTypeService(repository)


# Get all dive types
@api_router.get("/", response_model=List[MasterDiveTypeRead])
async def read_dive_types(service: MasterDiveTypeService = Depends(get_dive_type_service)):
    dive_types = await service.get_all_dive_types()
    return dive_types


# Get a single dive type by ID
@api_router.get("/{dive_type_id}", response_model=MasterDiveTypeRead)
async def read_dive_type(dive_type_id: int, service: MasterDiveTypeService = Depends(get_dive_type_service)):
    dive_type = await service.get_dive_type_by_id(dive_type_id)
    if not dive_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dive type not found")
    return dive_type


# Create a new dive type
@api_router.post("/", response_model=MasterDiveTypeRead, status_code=status.HTTP_201_CREATED)
async def create_dive_type(dive_type: MasterDiveTypeCreate, service: MasterDiveTypeService = Depends(get_dive_type_service)):
    created_dive_type = await service.create_dive_type(dive_type)
    return created_dive_type


# Update an existing dive type
@api_router.put("/{dive_type_id}", response_model=MasterDiveTypeRead)
async def update_dive_type(
    dive_type_id: int,
    dive_type_update: MasterDiveTypeUpdate,
    service: MasterDiveTypeService = Depends(get_dive_type_service)
):
    updated_dive_type = await service.update_dive_type(dive_type_id, dive_type_update)
    if not updated_dive_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dive type not found")
    return updated_dive_type


# Delete a dive type by ID
@api_router.delete("/{dive_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dive_type(dive_type_id: int, service: MasterDiveTypeService = Depends(get_dive_type_service)):
    success = await service.delete_dive_type(dive_type_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dive type not found")
    return
