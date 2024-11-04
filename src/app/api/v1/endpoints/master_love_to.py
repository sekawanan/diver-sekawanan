# app/api/v1/endpoints/master_love_to.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import logging

from app.schemas.base import BaseResponse
from app.schemas.master_love_to import MasterLoveToRead, MasterLoveToCreate, MasterLoveToUpdate
from app.services.master_love_to_service import MasterLoveToService
from app.dependencies import get_master_love_to_service

logger = logging.getLogger(__name__)

api_router = APIRouter(
    prefix="/master-love-tos",
    tags=["Master Love Tos"],
    responses={404: {"description": "Not found"}},
)

@api_router.post(
    "/",
    response_model=BaseResponse[MasterLoveToRead],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new master love to",
    description="Adds a new master love to to the system.",
)
async def create_master_love_to(
    master_love_to: MasterLoveToCreate,
    service: MasterLoveToService = Depends(get_master_love_to_service)
):
    """
    Create a new master love to.
    """
    try:
        created_master_love_to = await service.create_master_love_to(master_love_to)
        logger.info(f"Created master love to with ID: {created_master_love_to.id}")
        return created_master_love_to
    except ValueError as ve:
        logger.error(f"Error creating master love to: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )

@api_router.get(
    "/{love_to_id}",
    response_model=BaseResponse[MasterLoveToRead],
    status_code=status.HTTP_200_OK,
    summary="Retrieve a master love to by ID",
    description="Fetches a master love to by its unique ID.",
)
async def read_master_love_to(
    love_to_id: int,
    service: MasterLoveToService = Depends(get_master_love_to_service)
):
    """
    Retrieve a master love to by ID.
    """
    master_love_to = await service.get_master_love_to_by_id(love_to_id)
    if not master_love_to:
        logger.warning(f"Master love to with ID {love_to_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master love to not found."
        )
    logger.info(f"Retrieved master love to with ID: {love_to_id}")
    return master_love_to

@api_router.get(
    "/",
    response_model=BaseResponse[List[MasterLoveToRead]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all master love tos",
    description="Fetches a list of all master love tos.",
)
async def read_master_love_tos(
    service: MasterLoveToService = Depends(get_master_love_to_service)
):
    """
    Retrieve all master love tos with pagination.
    """
    master_love_tos = await service.get_all_master_love_tos()
    logger.info(f"Retrieved {len(master_love_tos)} master love tos.")
    return master_love_tos

@api_router.put(
    "/{love_to_id}",
    response_model=BaseResponse[MasterLoveToRead],
    status_code=status.HTTP_200_OK,
    summary="Update a master love to",
    description="Updates the details of an existing master love to.",
)
async def update_master_love_to(
    love_to_id: int,
    master_love_to_update: MasterLoveToUpdate,
    service: MasterLoveToService = Depends(get_master_love_to_service)
):
    """
    Update an existing master love to.
    """
    updated_master_love_to = await service.update_master_love_to(love_to_id, master_love_to_update)
    if not updated_master_love_to:
        logger.warning(f"Master love to with ID {love_to_id} not found for update.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master love to not found."
        )
    logger.info(f"Updated master love to with ID: {love_to_id}")
    return updated_master_love_to

@api_router.delete(
    "/{love_to_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a master love to",
    description="Removes a master love to from the system.",
)
async def delete_master_love_to(
    love_to_id: int,
    service: MasterLoveToService = Depends(get_master_love_to_service)
):
    """
    Delete a master love to.
    """
    success = await service.delete_master_love_to(love_to_id)
    if not success:
        logger.warning(f"Master love to with ID {love_to_id} not found for deletion.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master love to not found."
        )
    logger.info(f"Deleted master love to with ID: {love_to_id}")
    return