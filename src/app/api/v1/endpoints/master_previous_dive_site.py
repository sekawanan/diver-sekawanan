# app/api/v1/endpoints/master_previous_dive_site.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import logging

from app.schemas.base_response import BaseResponse
from app.schemas.master_previous_dive_site import MasterPreviousDiveSiteRead, MasterPreviousDiveSiteCreate
from app.services.master_previous_dive_site_service import MasterPreviousDiveSiteService
from app.dependencies import get_master_previous_dive_site_service
from app.utils.responses import create_success_response

logger = logging.getLogger(__name__)

api_router = APIRouter(
    prefix="/master-previous-dive-sites",
    tags=["Master Previous Dive Sites"],
    responses={404: {"description": "Not found"}},
)

@api_router.post(
    "/",
    response_model=BaseResponse[MasterPreviousDiveSiteRead],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new master previous dive site",
    description="Adds a new master previous dive site to the system.",
)
async def create_master_previous_dive_site(
    dive_site: MasterPreviousDiveSiteCreate,
    service: MasterPreviousDiveSiteService = Depends(get_master_previous_dive_site_service)
):
    """
    Create a new master previous dive site.
    """
    try:
        created_dive_site = await service.create_master_previous_dive_site(dive_site)
        logger.info(f"Created master previous dive site with ID: {created_dive_site.id}")
        return create_success_response(MasterPreviousDiveSiteRead.from_orm(created_dive_site))
    except ValueError as ve:
        logger.error(f"Error creating master previous dive site: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )

@api_router.get(
    "/{dive_site_id}",
    response_model=BaseResponse[MasterPreviousDiveSiteRead],
    status_code=status.HTTP_200_OK,
    summary="Retrieve a master previous dive site by ID",
    description="Fetches a master previous dive site by its unique ID.",
)
async def read_master_previous_dive_site(
    dive_site_id: int,
    service: MasterPreviousDiveSiteService = Depends(get_master_previous_dive_site_service)
):
    """
    Retrieve a master previous dive site by ID.
    """
    dive_site = await service.get_master_previous_dive_site_by_id(dive_site_id)
    if not dive_site:
        logger.warning(f"Master previous dive site with ID {dive_site_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master previous dive site not found."
        )
    logger.info(f"Retrieved master previous dive site with ID: {dive_site_id}")
    return create_success_response(MasterPreviousDiveSiteRead.from_orm(dive_site))

@api_router.get(
    "/",
    response_model=BaseResponse[List[MasterPreviousDiveSiteRead]],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all master previous dive sites",
    description="Fetches a list of all master previous dive sites.",
)
async def read_master_previous_dive_sites(
    service: MasterPreviousDiveSiteService = Depends(get_master_previous_dive_site_service)
):
    """
    Retrieve all master previous dive sites with pagination.
    """
    dive_sites = await service.get_all_master_previous_dive_sites()
    logger.info(f"Retrieved {len(dive_sites)} master previous dive sites.")
    return create_success_response(dive_sites)

@api_router.put(
    "/{dive_site_id}",
    response_model=BaseResponse[MasterPreviousDiveSiteRead],
    status_code=status.HTTP_200_OK,
    summary="Update a master previous dive site",
    description="Updates the details of an existing master previous dive site.",
)
# async def update_master_previous_dive_site(
#     dive_site_id: int,
#     dive_site_update: MasterPreviousDiveSiteUpdate,
#     service: MasterPreviousDiveSiteService = Depends(get_master_previous_dive_site_service)
# ):
#     """
#     Update an existing master previous dive site.
#     """
#     updated_dive_site = await service.update_master_previous_dive_site(dive_site_id, dive_site_update)
#     if not updated_dive_site:
#         logger.warning(f"Master previous dive site with ID {dive_site_id} not found for update.")
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Master previous dive site not found."
#         )
#     logger.info(f"Updated master previous dive site with ID: {dive_site_id}")
#     return updated_dive_site

@api_router.delete(
    "/{dive_site_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a master previous dive site",
    description="Removes a master previous dive site from the system.",
)
async def delete_master_previous_dive_site(
    dive_site_id: int,
    service: MasterPreviousDiveSiteService = Depends(get_master_previous_dive_site_service)
):
    """
    Delete a master previous dive site.
    """
    success = await service.delete_master_previous_dive_site(dive_site_id)
    if not success:
        logger.warning(f"Master previous dive site with ID {dive_site_id} not found for deletion.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master previous dive site not found."
        )
    logger.info(f"Deleted master previous dive site with ID: {dive_site_id}")
    return