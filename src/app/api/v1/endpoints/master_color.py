# app/api/v1/endpoints/master_color.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.master_color import MasterColorRead
from app.services.master_color_service import MasterColorService
from app.database.session import get_db
from app.dependencies import get_master_color_service

api_router = APIRouter()


@api_router.get(
        "/", 
        response_model=List[MasterColorRead],
        status_code=status.HTTP_200_OK,
        summary="Retrieve all master gears available",
)

async def read_master_colors(
    service: MasterColorService = Depends(get_master_color_service)
):
    """
    Retrieve all master colors.
    """
    try:
        gears = await service.get_all_master_colors()
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