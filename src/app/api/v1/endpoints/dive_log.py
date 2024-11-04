# app/api/v1/endpoints/dive_log.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.base import BaseResponse
from app.schemas.dive_log import DiveLogRead, DiveLogCreate, DiveLogUpdate
from app.services.dive_log_service import DiveLogService
from app.repositories.dive_log_repository import DiveLogRepository
from app.database.session import get_db

api_router = APIRouter()


def get_dive_log_service(db: AsyncSession = Depends(get_db)) -> DiveLogService:
    repository = DiveLogRepository(db)
    return DiveLogService(repository)


@api_router.get("/dive-logs", response_model=BaseResponse[List[DiveLogRead]])
async def read_dive_logs(service: DiveLogService = Depends(get_dive_log_service)):
    dive_logs = await service.get_all_dive_logs()
    return BaseResponse(status="success", data=dive_logs)


@api_router.get("/dive-logs/{dive_log_id}", response_model=BaseResponse[DiveLogRead])
async def read_dive_log(dive_log_id: int, service: DiveLogService = Depends(get_dive_log_service)):
    dive_log = await service.get_dive_log_by_id(dive_log_id)
    if not dive_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dive log not found")
    return BaseResponse(status="success", data=dive_log)


@api_router.post("/dive-logs", response_model=BaseResponse[DiveLogRead], status_code=status.HTTP_201_CREATED)
async def create_dive_log(dive_log: DiveLogCreate, service: DiveLogService = Depends(get_dive_log_service)):
    created_dive_log = await service.create_dive_log(dive_log)
    return BaseResponse(status="success", data=created_dive_log)


@api_router.put("/dive-logs/{dive_log_id}", response_model=BaseResponse[DiveLogRead])
async def update_dive_log(
    dive_log_id: int,
    dive_log_update: DiveLogUpdate,
    service: DiveLogService = Depends(get_dive_log_service)
):
    updated_dive_log = await service.update_dive_log(dive_log_id, dive_log_update)
    if not updated_dive_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dive log not found")
    return BaseResponse(status="success", data=updated_dive_log)


@api_router.delete("/dive-logs/{dive_log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dive_log(dive_log_id: int, service: DiveLogService = Depends(get_dive_log_service)):
    success = await service.delete_dive_log(dive_log_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dive log not found")
    return
