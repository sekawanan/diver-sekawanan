# app/services/diver_license_service.py

from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.diver_license_repository import DiverLicenseRepository
from app.repositories.diver_profile_repository import DiverProfileRepository
from app.repositories.master_license_repository import MasterLicenseRepository
from app.schemas.diver_license import DiverLicenseCreate
from app.models import DiverLicense
from app.schemas.diver_profile import DiverProfileBase  # Ensure this is your SQLAlchemy model

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

    async def create_diver_license(self, user_id: str, license_data: DiverLicenseCreate) -> DiverLicense:
        diver_profile = await self.profile_repository.get_diver_profile(user_id)
        if not diver_profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver profile not found")

        new_license = await self.license_repository.create_license(diver_profile.id, license_data)
        return DiverProfileBase.from_orm(new_license)

    async def get_all_diver_licenses(self, user_id: str) -> List[DiverLicense]:
        diver_profile = await self.profile_repository.get_diver_profile(user_id)
        if not diver_profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver profile not found")

        licenses = await self.license_repository.get_all_licenses_by_diver_profile_id(diver_profile.id)
        return [DiverProfileBase.from_orm(license) for license in licenses]
