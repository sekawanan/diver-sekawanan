# app/api/v1/endpoints/diver_license.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.base_response import BaseResponse
from app.schemas.diver_license import DiverLicenseCreate, DiverLicenseRead, DiverLicenseUpdate
from app.dependencies import get_diver_license_service
from app.services.diver_license_service import DiverLicenseService  # For type hinting

api_router = APIRouter()

@api_router.post(
    "/diver-profiles/{diver_profile_id}/licenses",
    response_model=BaseResponse[DiverLicenseRead],
    status_code=status.HTTP_201_CREATED
)
async def create_diver_license(
    diver_profile_id: int,
    diver_license_data: DiverLicenseCreate,
    service: DiverLicenseService = Depends(get_diver_license_service)
):
    """
    Create a new diver license associated with a specific diver profile.
    """
    new_license = await service.create_diver_license(diver_profile_id, diver_license_data)
    license_read = DiverLicenseRead.from_orm(new_license)
    return BaseResponse(status="success", data=license_read)

@api_router.get(
    "/",
    response_model=List[DiverLicenseRead],
    status_code=status.HTTP_200_OK
)
async def read_diver_licenses(
    service: DiverLicenseService = Depends(get_diver_license_service)
):
    """
    Retrieve all diver licenses.
    """
    licenses = await service.get_all_diver_licenses()
    return licenses

@api_router.get(
    "/{diver_license_id}",
    response_model=DiverLicenseRead,
    status_code=status.HTTP_200_OK
)
async def read_diver_license(
    diver_license_id: int,
    service: DiverLicenseService = Depends(get_diver_license_service)
):
    """
    Retrieve a specific diver license by its ID.
    """
    license = await service.get_diver_license_by_id(diver_license_id)
    if not license:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver license not found")
    return license

@api_router.get(
    "/diver-profiles/{diver_profile_id}/licenses",
    response_model=List[DiverLicenseRead],
    status_code=status.HTTP_200_OK
)
async def read_diver_licenses_by_profile_id(
    diver_profile_id: int,
    service: DiverLicenseService = Depends(get_diver_license_service)
):
    """
    Retrieve all diver licenses associated with a specific diver profile ID.
    """
    licenses = await service.get_diver_licenses_by_profile_id(diver_profile_id)
    if not licenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No licenses found for diver_profile_id {diver_profile_id}"
        )
    return licenses

@api_router.get(
    "/diver-profiles/{diver_profile_id}/latest_license",
    response_model=DiverLicenseRead,
    status_code=status.HTTP_200_OK
)
async def read_diver_latest_license_by_profile_id(
    diver_profile_id: int,
    service: DiverLicenseService = Depends(get_diver_license_service)
):
    """
    Retrieve the latest or verified license associated with a specific diver profile ID.
    """
    latest_license = await service.get_diver_latest_license_by_profile_id(diver_profile_id)
    if not latest_license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No latest license found for diver_profile_id {diver_profile_id}"
        )
    return latest_license

@api_router.put(
    "/{diver_license_id}",
    response_model=DiverLicenseRead,
    status_code=status.HTTP_200_OK
)
async def update_diver_license(
    diver_license_id: int,
    diver_license_update: DiverLicenseUpdate,
    service: DiverLicenseService = Depends(get_diver_license_service)
):
    """
    Update an existing diver license by its ID.
    """
    updated_license = await service.update_diver_license(diver_license_id, diver_license_update)
    if not updated_license:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver license not found")
    return DiverLicenseRead.from_orm(updated_license)

@api_router.delete(
    "/{diver_license_id}",
    response_model=BaseResponse[None],
    status_code=status.HTTP_200_OK
)
async def delete_diver_license(
    diver_license_id: int,
    service: DiverLicenseService = Depends(get_diver_license_service)
):
    """
    Delete a diver license by its ID.
    """
    success = await service.delete_diver_license(diver_license_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver license not found")
    return BaseResponse(status="success", message="Diver license deleted successfully")