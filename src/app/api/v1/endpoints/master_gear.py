# app/api/v1/endpoints/master_gear.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.master_gear import MasterGearRead
from app.services.master_gear_service import MasterGearService
from app.dependencies import get_master_gear_service
import logging

logger = logging.getLogger(__name__)

api_router = APIRouter()

@api_router.get(
        "/", 
        response_model=List[MasterGearRead],
        status_code=status.HTTP_200_OK,
        summary="Retrieve all master gears available",
)

async def read_master_gears(
    service: MasterGearService = Depends(get_master_gear_service)
):
    """
    Retrieve all master gears.
    """
    try:
        gears = await service.get_all_master_gears()
        if not gears:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No master gears found.",
            )
        return gears
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving master gears entries.",
        ) from e