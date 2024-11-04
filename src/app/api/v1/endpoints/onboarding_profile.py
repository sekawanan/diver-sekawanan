# app/api/v1/endpoints/onboarding_profile.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, status
import logging

from app.api.dependencies import get_current_user_id
from app.schemas.base import BaseResponse
from app.schemas.onboarding_profile import (
    OnboardingProfileRead,
    OnboardingProfileCreate,
    OnboardingProfileUpdate,
    OnboardingProfileCreateRequest,
    OnboardingProfileWithRelations
)
from app.services.onboarding_profile_service import OnboardingProfileService
from app.dependencies import get_onboarding_profile_service

logger = logging.getLogger(__name__)

api_router = APIRouter(
    prefix="/onboarding-profiles",
    tags=["Onboarding Profiles"],
    responses={404: {"description": "Not found"}},
)

@api_router.post(
    "/",
    response_model=BaseResponse[OnboardingProfileWithRelations],  # Updated response model
    status_code=status.HTTP_201_CREATED,
    summary="Create a new onboarding profile",
    description="Adds a new onboarding profile to the system along with associated profile love tos and profile previous dive sites.",
)
async def create_onboarding_profile(
    onboarding_profile: OnboardingProfileCreateRequest,
    service: OnboardingProfileService = Depends(get_onboarding_profile_service)
):
    """
    Create a new onboarding profile along with associated profile love tos and profile previous dive sites.
    """
    try:
        created_profile = await service.create_onboarding_profile_with_associations(onboarding_profile)
        logger.info(f"Created onboarding profile with ID: {created_profile.id}")
        return BaseResponse(status="success", data=created_profile)
    except HTTPException as he:
        logger.error(f"Error creating onboarding profile: {he.detail}")
        raise BaseResponse(status="error", data=he)
    except Exception as e:
        logger.error(f"Unexpected error creating onboarding profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the onboarding profile."
        )
    
@api_router.post(
    "/me",
    response_model=BaseResponse[OnboardingProfileWithRelations],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new onboarding profile",
    description="Adds a new onboarding profile to the system along with associated profile love tos and profile previous dive sites.",
)
async def create_onboarding_profile(
    onboarding_profile: OnboardingProfileCreateRequest,
    user_id: str = Depends(get_current_user_id),
    service: OnboardingProfileService = Depends(get_onboarding_profile_service)
):
    """
    Create a new onboarding profile along with associated profile love tos and profile previous dive sites.
    """
    try:
        created_profile = await service.create_onboarding_profile_with_associations(onboarding_profile, user_id=user_id)
        logger.info(f"Created onboarding profile with ID: {created_profile.id}")
        return BaseResponse(status="success", data=created_profile)
    except HTTPException as he:
        logger.error(f"Error creating onboarding profile: {he.detail}")
        raise BaseResponse(status="error", data=he)
    except Exception as e:
        logger.error(f"Unexpected error creating onboarding profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the onboarding profile."
        )

@api_router.get(
    "/me",
    response_model=BaseResponse[OnboardingProfileWithRelations],  # Updated response model
    status_code=status.HTTP_200_OK,
    summary="Retrieve an onboarding self profile",
    description="Fetches an onboarding profile by access token.",
)
async def read_onboarding_profile(
    user_id: str = Depends(get_current_user_id),
    service: OnboardingProfileService = Depends(get_onboarding_profile_service),
):
    """
    Retrieve an onboarding profile by ID.
    """
    profile = await service.get_onboarding_profile_by_user_id(user_id)
    if not profile:
        logger.warning(f"Onboarding profile for user_id '{user_id}' not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onboarding profile not found."
        )
    logger.info(f"Retrieved onboarding profile for user_id: {user_id}")
    return BaseResponse(status="success", data=profile)

@api_router.put(
    "/me",
    response_model=BaseResponse[OnboardingProfileWithRelations],  # Updated response model
    status_code=status.HTTP_200_OK,
    summary="Update an onboarding profile",
    description="Updates the details of an existing onboarding profile.",
)

async def update_onboarding_profile(
    profile_update: OnboardingProfileUpdate,
    user_id: str = Depends(get_current_user_id),
    service: OnboardingProfileService = Depends(get_onboarding_profile_service)
):
    """
    Update an existing onboarding profile along with its associated profile love tos and profile previous dive sites.
    """
    try:
        updated_profile = await service.update_onboarding_profile(user_id, profile_update)
        logger.info(f"Updated onboarding profile with ID: {updated_profile.id}")
        return BaseResponse(status="success", data=updated_profile)
    except HTTPException as he:
        logger.error(f"Error updating onboarding profile: {he.detail}")
        raise BaseResponse(status="success", data=he)
    except Exception as e:
        logger.error(f"Unexpected error updating onboarding profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the onboarding profile."
        )

@api_router.get(
    "/",
    response_model=BaseResponse[OnboardingProfileWithRelations],  # Updated response model
    status_code=status.HTTP_200_OK,
    summary="Retrieve all onboarding profiles",
    description="Fetches a list of all onboarding profiles.",
)
async def read_onboarding_profiles(
    skip: int = 0,
    limit: int = 100,
    service: OnboardingProfileService = Depends(get_onboarding_profile_service)
):
    """
    Retrieve all onboarding profiles with pagination.
    """
    profiles = await service.get_all_onboarding_profiles(skip=skip, limit=limit)
    logger.info(f"Retrieved {len(profiles)} onboarding profiles.")
    return BaseResponse(status="success", data=profiles)

# @api_router.get(
#     "/{profile_id}",
#     response_model=OnboardingProfileWithRelations,  # Updated response model
#     status_code=status.HTTP_200_OK,
#     summary="Retrieve an onboarding profile by ID",
#     description="Fetches an onboarding profile by its unique ID.",
# )
# async def read_onboarding_profile(
#     profile_id: int,
#     service: OnboardingProfileService = Depends(get_onboarding_profile_service),
# ):
#     """
#     Retrieve an onboarding profile by ID.
#     """
#     profile = await service.get_onboarding_profile_by_id(profile_id)
#     if not profile:
#         logger.warning(f"Onboarding profile with ID {profile_id} not found.")
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Onboarding profile not found."
#         )
#     logger.info(f"Retrieved onboarding profile with ID: {profile_id}")
#     return profile

# @api_router.put(
#     "/{profile_id}",
#     response_model=OnboardingProfileWithRelations,  # Updated response model
#     status_code=status.HTTP_200_OK,
#     summary="Update an onboarding profile",
#     description="Updates the details of an existing onboarding profile.",
# )

# async def update_onboarding_profile(
#     profile_id: int,
#     profile_update: OnboardingProfileUpdate,
#     service: OnboardingProfileService = Depends(get_onboarding_profile_service)
# ):
#     """
#     Update an existing onboarding profile along with its associated profile love tos and profile previous dive sites.
#     """
#     try:
#         updated_profile = await service.update_onboarding_profile(profile_id, profile_update)
#         logger.info(f"Updated onboarding profile with ID: {updated_profile.id}")
#         return updated_profile
#     except HTTPException as he:
#         logger.error(f"Error updating onboarding profile: {he.detail}")
#         raise he
#     except Exception as e:
#         logger.error(f"Unexpected error updating onboarding profile: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An unexpected error occurred while updating the onboarding profile."
#         )

# @api_router.delete(
#     "/{profile_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     summary="Delete an onboarding profile",
#     description="Removes an onboarding profile from the system along with its associations.",
# )
# async def delete_onboarding_profile(
#     profile_id: int,
#     service: OnboardingProfileService = Depends(get_onboarding_profile_service)
# ):
#     """
#     Delete an onboarding profile along with its associated profile love tos and profile previous dive sites.
#     """
#     try:
#         success = await service.delete_onboarding_profile(profile_id)
#         if not success:
#             logger.warning(f"Onboarding profile with ID {profile_id} not found for deletion.")
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Onboarding profile not found."
#             )
#         logger.info(f"Deleted onboarding profile with ID: {profile_id}")
#         return
#     except HTTPException as he:
#         logger.error(f"Error deleting onboarding profile: {he.detail}")
#         raise he
#     except Exception as e:
#         logger.error(f"Unexpected error deleting onboarding profile: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An unexpected error occurred while deleting the onboarding profile."
#         )