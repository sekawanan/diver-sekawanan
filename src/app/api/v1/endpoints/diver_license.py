# app/api/v1/endpoints/diver_license.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.dependencies import get_current_user_id
from app.schemas.base_response import BaseResponse
from app.schemas.diver_license import DiverLicenseBase, DiverLicenseCreate
from app.dependencies import get_diver_license_service
from app.services.diver_license_service import DiverLicenseService
from app.utils.responses import create_success_response  # For type hinting

api_router = APIRouter()

@api_router.post(
    "/diver-licenses/me",
    response_model=BaseResponse[DiverLicenseBase],
    status_code=status.HTTP_201_CREATED
)
async def create_diver_license(
    diver_license_data: DiverLicenseCreate,
    user_id: str = Depends(get_current_user_id),
    service: DiverLicenseService = Depends(get_diver_license_service)
):
    """
    Create a new diver license associated with a specific diver profile.
    """
    new_license = await service.create_diver_license(user_id, diver_license_data)
    return create_success_response(new_license)

@api_router.get(
    "/diver-licenses/me",
    response_model=List[DiverLicenseBase],
    status_code=status.HTTP_200_OK
)
async def read_diver_licenses(
    user_id: str = Depends(get_current_user_id),
    service: DiverLicenseService = Depends(get_diver_license_service)
):
    """
    Retrieve all diver licenses.
    """
    licenses = await service.get_all_diver_licenses(user_id)
    return licenses