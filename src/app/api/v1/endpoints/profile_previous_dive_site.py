# app/api/v1/endpoints/profile_previous_dive_site.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import logging

from app.schemas.profile_previous_dive_site import ProfilePreviousDiveSiteRead, ProfilePreviousDiveSiteCreate, ProfilePreviousDiveSiteUpdate
from app.services.profile_previous_dive_site_service import ProfilePreviousDiveSiteService
from app.dependencies import get_profile_previous_dive_site_service

logger = logging.getLogger(__name__)

api_router = APIRouter(
    prefix="/profile-previous-dive-sites",
    tags=["Profile Previous Dive Sites"],
    responses={404: {"description": "Not found"}},
)

@api_router.post(
    "/",
    response_model=ProfilePreviousDiveSiteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new profile previous dive site",
    description="Adds a new profile previous dive site to the system.",
)
async def create_profile_previous_dive_site(
    dive_site: ProfilePreviousDiveSiteCreate,
    service: ProfilePreviousDiveSiteService = Depends(get_profile_previous_dive_site_service)
):
    """
    Create a new profile previous dive site.
    """
    try:
        created_dive_site = await service.create_profile_previous_dive_site(dive_site)
        logger.info(f"Created profile previous dive site with ID: {created_dive_site.id}")
        return created_dive_site
    except ValueError as ve:
        logger.error(f"Error creating profile previous dive site: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )

@api_router.get(
    "/{dive_site_id}",
    response_model=ProfilePreviousDiveSiteRead,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a profile previous dive site by ID",
    description="Fetches a profile previous dive site by its unique ID.",
)
async def read_profile_previous_dive_site(
    dive_site_id: int,
    service: ProfilePreviousDiveSiteService = Depends(get_profile_previous_dive_site_service)
):
    """
    Retrieve a profile previous dive site by ID.
    """
    dive_site = await service.get_profile_previous_dive_site_by_id(dive_site_id)
    if not dive_site:
        logger.warning(f"Profile previous dive site with ID {dive_site_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile previous dive site not found."
        )
    logger.info(f"Retrieved profile previous dive site with ID: {dive_site_id}")
    return dive_site

@api_router.get(
    "/",
    response_model=List[ProfilePreviousDiveSiteRead],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all profile previous dive sites",
    description="Fetches a list of all profile previous dive sites.",
)
async def read_profile_previous_dive_sites(
    skip: int = 0,
    limit: int = 100,
    service: ProfilePreviousDiveSiteService = Depends(get_profile_previous_dive_site_service)
):
    """
    Retrieve all profile previous dive sites with pagination.
    """
    dive_sites = await service.get_all_profile_previous_dive_sites(skip=skip, limit=limit)
    logger.info(f"Retrieved {len(dive_sites)} profile previous dive sites.")
    return dive_sites

@api_router.put(
    "/{dive_site_id}",
    response_model=ProfilePreviousDiveSiteRead,
    status_code=status.HTTP_200_OK,
    summary="Update a profile previous dive site",
    description="Updates the details of an existing profile previous dive site.",
)
async def update_profile_previous_dive_site(
    dive_site_id: int,
    dive_site_update: ProfilePreviousDiveSiteUpdate,
    service: ProfilePreviousDiveSiteService = Depends(get_profile_previous_dive_site_service)
):
    """
    Update an existing profile previous dive site.
    """
    updated_dive_site = await service.update_profile_previous_dive_site(dive_site_id, dive_site_update)
    if not updated_dive_site:
        logger.warning(f"Profile previous dive site with ID {dive_site_id} not found for update.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile previous dive site not found."
        )
    logger.info(f"Updated profile previous dive site with ID: {dive_site_id}")
    return updated_dive_site

@api_router.delete(
    "/{dive_site_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a profile previous dive site",
    description="Removes a profile previous dive site from the system.",
)
async def delete_profile_previous_dive_site(
    dive_site_id: int,
    service: ProfilePreviousDiveSiteService = Depends(get_profile_previous_dive_site_service)
):
    """
    Delete a profile previous dive site.
    """
    success = await service.delete_profile_previous_dive_site(dive_site_id)
    if not success:
        logger.warning(f"Profile previous dive site with ID {dive_site_id} not found for deletion.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile previous dive site not found."
        )
    logger.info(f"Deleted profile previous dive site with ID: {dive_site_id}")
    return