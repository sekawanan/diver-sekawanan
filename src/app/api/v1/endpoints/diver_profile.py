# app/api/v1/endpoints/diver_profile.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import logging

from app.api.dependencies import get_current_user_id
from app.schemas import (
    DiverProfileCreate,
    DiverProfileRead,
    DiverProfileUpdate,
    DiverInfoResponse,
    DiverInfoData,
    DiverLicenseRead,
    DivePreferenceRead,
    DiverGearRead
)
from app.schemas.base_response import BaseResponse
from app.services.diver_profile_service import DiverProfileService
from app.dependencies import get_diver_profile_service
from app.utils.responses import create_success_response

api_router = APIRouter()
logger = logging.getLogger(__name__)

@api_router.post("/diver-profiles/me", response_model=BaseResponse[DiverProfileRead], status_code=status.HTTP_201_CREATED)
async def create_diver_profile(
    diver_profile: DiverProfileCreate,
    user_id: str = Depends(get_current_user_id),
    service: DiverProfileService = Depends(get_diver_profile_service)
):
    logger.info(f"Received diver_profile: {diver_profile}")
    created_profile = await service.create_diver_profile(user_id, diver_profile)
    return create_success_response(created_profile)

@api_router.get("/diver-profiles/me", response_model=BaseResponse[DiverProfileRead])
async def read_diver_profile(
    user_id: str = Depends(get_current_user_id),
    service: DiverProfileService = Depends(get_diver_profile_service)
):
    profile = await service.get_diver_profile(user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver profile not found")
    return create_success_response(profile)

@api_router.put("/diver-profiles/me", response_model=BaseResponse[DiverProfileRead])
async def update_diver_profile(
    diver_profile: DiverProfileUpdate,
    user_id: str = Depends(get_current_user_id),
    service: DiverProfileService = Depends(get_diver_profile_service)
):
    updated_profile = await service.update_diver_profile(user_id, diver_profile)
    if not updated_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver profile not found")
    return create_success_response(updated_profile)

@api_router.delete("/diver-profiles/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diver_profile(
    user_id: str = Depends(get_current_user_id),
    service: DiverProfileService = Depends(get_diver_profile_service)
):
    success = await service.delete_diver_profile(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver profile not found")
    return

# New route for nested JSON response
@api_router.get("/diver-profiles/me/info", response_model=BaseResponse[DiverInfoResponse])
async def get_diver_profile_info(
    user_id: str = Depends(get_current_user_id),
    service: DiverProfileService = Depends(get_diver_profile_service)
):
    profile = await service.get_diver_profile(user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver profile not found")
    
    # Construct DiverInfoData using from_orm for nested relationships
    data = DiverInfoData(
        profile=DiverProfileRead.from_orm(profile),
        licenses=[DiverLicenseRead.from_orm(license) for license in profile.diver_licenses],
        dive_preferences=[DivePreferenceRead.from_orm(pref) for pref in profile.dive_preferences],
        diver_gears=[DiverGearRead.from_orm(gear) for gear in profile.diver_gears]
    )
    
    # Construct and return the response
    response = DiverInfoResponse(
        status="success",
        message="Diver info fetched successfully",
        data=data
    )
    return response

# @api_router.get("/diver-profiles/{diver_profile_id}", response_model=DiverProfileRead)
# async def read_diver_profile(
#     diver_profile_id: int,
#     service: DiverProfileService = Depends(get_diver_profile_service)
# ):
#     profile = await service.get_diver_profile(diver_profile_id)
#     if not profile:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver profile not found")
#     return DiverProfileRead.from_orm(profile)

# @api_router.put("/diver-profiles/{diver_profile_id}", response_model=DiverProfileRead)
# async def update_diver_profile(
#     diver_profile_id: int,
#     diver_profile: DiverProfileUpdate,
#     service: DiverProfileService = Depends(get_diver_profile_service)
# ):
#     updated_profile = await service.update_diver_profile(diver_profile_id, diver_profile)
#     if not updated_profile:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver profile not found")
#     return DiverProfileRead.from_orm(updated_profile)

# @api_router.delete("/diver-profiles/{diver_profile_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_diver_profile(
#     diver_profile_id: int,
#     service: DiverProfileService = Depends(get_diver_profile_service)
# ):
#     success = await service.delete_diver_profile(diver_profile_id)
#     if not success:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver profile not found")
#     return

# # New route for nested JSON response
# @api_router.get("/diver-profiles/{diver_profile_id}/info", response_model=DiverInfoResponse)
# async def get_diver_profile_info(
#     diver_profile_id: int,
#     service: DiverProfileService = Depends(get_diver_profile_service)
# ):
#     profile = await service.get_diver_profile(diver_profile_id)
#     if not profile:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver profile not found")
    
#     # Construct DiverInfoData using from_orm for nested relationships
#     data = DiverInfoData(
#         profile=DiverProfileRead.from_orm(profile),
#         licenses=[DiverLicenseRead.from_orm(license) for license in profile.diver_licenses],
#         dive_preferences=[DivePreferenceRead.from_orm(pref) for pref in profile.dive_preferences],
#         diver_gears=[DiverGearRead.from_orm(gear) for gear in profile.diver_gears]
#     )
    
#     # Construct and return the response
#     response = DiverInfoResponse(
#         status="success",
#         message="Diver info fetched successfully",
#         data=data
#     )
#     return response