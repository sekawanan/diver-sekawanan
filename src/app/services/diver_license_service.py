# app/services/diver_license_service.py

from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.diver_license_repository import DiverLicenseRepository
from app.repositories.diver_profile_repository import DiverProfileRepository
from app.repositories.master_license_repository import MasterLicenseRepository
from app.schemas.diver_license import DiverLicenseCreate, DiverLicenseUpdate
from app.models import DiverLicense  # Ensure this is your SQLAlchemy model

class DiverLicenseService:
    def __init__(
        self,
        license_repository: DiverLicenseRepository,
        profile_repository: DiverProfileRepository,
        master_license_repository: MasterLicenseRepository
    ):
        self.license_repository = license_repository
        self.profile_repository = profile_repository
        self.master_license_repository = master_license_repository

    async def create_diver_license(self, diver_profile_id: int, license_data: DiverLicenseCreate) -> DiverLicense:
        # Validate diver_profile exists
        diver_profile = await self.profile_repository.get_profile_by_id(diver_profile_id)
        if not diver_profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver profile not found")

        # Validate master_license exists
        master_license = await self.master_license_repository.get_license_by_id(license_data.master_license_id)
        if not master_license:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Master license not found")

        # Create new diver license
        new_license = await self.license_repository.create_license(diver_profile_id, license_data)
        return new_license

    async def get_all_diver_licenses(self) -> List[DiverLicense]:
        return await self.license_repository.get_all_licenses()

    async def get_diver_license_by_id(self, license_id: int) -> Optional[DiverLicense]:
        return await self.license_repository.get_license_by_id(license_id)

    async def get_diver_licenses_by_profile_id(self, diver_profile_id: int) -> List[DiverLicense]:
        return await self.license_repository.get_licenses_by_profile_id(diver_profile_id)

    async def get_diver_latest_license_by_profile_id(self, diver_profile_id: int) -> Optional[DiverLicense]:
        return await self.license_repository.get_latest_license_by_profile_id(diver_profile_id)

    async def update_diver_license(self, license_id: int, license_update: DiverLicenseUpdate) -> Optional[DiverLicense]:
        return await self.license_repository.update_license(license_id, license_update)

    async def delete_diver_license(self, license_id: int) -> bool:
        return await self.license_repository.delete_license(license_id)