# app/api/v1/endpoints/profile_love_to.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import logging

from app.schemas.profile_love_to import ProfileLoveToRead, ProfileLoveToCreate, ProfileLoveToUpdate
from app.services.profile_love_to_service import ProfileLoveToService
from app.dependencies import get_profile_love_to_service

logger = logging.getLogger(__name__)

api_router = APIRouter(
    prefix="/profile-love-tos",
    tags=["Profile Love Tos"],
    responses={404: {"description": "Not found"}},
)

@api_router.post(
    "/",
    response_model=ProfileLoveToRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new profile love to",
    description="Adds a new profile love to to the system.",
)
async def create_profile_love_to(
    profile_love_to: ProfileLoveToCreate,
    service: ProfileLoveToService = Depends(get_profile_love_to_service)
):
    """
    Create a new profile love to.
    """
    try:
        created_profile_love_to = await service.create_profile_love_to(profile_love_to)
        logger.info(f"Created profile love to with ID: {created_profile_love_to.id}")
        return created_profile_love_to
    except ValueError as ve:
        logger.error(f"Error creating profile love to: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )

@api_router.get(
    "/{love_to_id}",
    response_model=ProfileLoveToRead,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a profile love to by ID",
    description="Fetches a profile love to by its unique ID.",
)
async def read_profile_love_to(
    love_to_id: int,
    service: ProfileLoveToService = Depends(get_profile_love_to_service)
):
    """
    Retrieve a profile love to by ID.
    """
    profile_love_to = await service.get_profile_love_to_by_id(love_to_id)
    if not profile_love_to:
        logger.warning(f"Profile love to with ID {love_to_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile love to not found."
        )
    logger.info(f"Retrieved profile love to with ID: {love_to_id}")
    return profile_love_to

@api_router.get(
    "/",
    response_model=List[ProfileLoveToRead],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all profile love tos",
    description="Fetches a list of all profile love tos.",
)
async def read_profile_love_tos(
    skip: int = 0,
    limit: int = 100,
    service: ProfileLoveToService = Depends(get_profile_love_to_service)
):
    """
    Retrieve all profile love tos with pagination.
    """
    profile_love_tos = await service.get_all_profile_love_tos(skip=skip, limit=limit)
    logger.info(f"Retrieved {len(profile_love_tos)} profile love tos.")
    return profile_love_tos

@api_router.put(
    "/{love_to_id}",
    response_model=ProfileLoveToRead,
    status_code=status.HTTP_200_OK,
    summary="Update a profile love to",
    description="Updates the details of an existing profile love to.",
)
async def update_profile_love_to(
    love_to_id: int,
    profile_love_to_update: ProfileLoveToUpdate,
    service: ProfileLoveToService = Depends(get_profile_love_to_service)
):
    """
    Update an existing profile love to.
    """
    updated_profile_love_to = await service.update_profile_love_to(love_to_id, profile_love_to_update)
    if not updated_profile_love_to:
        logger.warning(f"Profile love to with ID {love_to_id} not found for update.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile love to not found."
        )
    logger.info(f"Updated profile love to with ID: {love_to_id}")
    return updated_profile_love_to

@api_router.delete(
    "/{love_to_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a profile love to",
    description="Removes a profile love to from the system.",
)
async def delete_profile_love_to(
    love_to_id: int,
    service: ProfileLoveToService = Depends(get_profile_love_to_service)
):
    """
    Delete a profile love to.
    """
    success = await service.delete_profile_love_to(love_to_id)
    if not success:
        logger.warning(f"Profile love to with ID {love_to_id} not found for deletion.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile love to not found."
        )
    logger.info(f"Deleted profile love to with ID: {love_to_id}")
    return