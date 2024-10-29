# app/services/master_license_service.py
from typing import List
from app.repositories.master_license_repository import MasterLicenseRepository
from app.models.master_license import MasterLicense

class MasterLicenseService:
    def __init__(self, repository: MasterLicenseRepository):
        self.repository = repository

    async def get_all_master_licenses(self) -> List[MasterLicense]:
        return await self.repository.get_all_master_licenses()

    async def create_master_license(self, license_data: MasterLicense) -> MasterLicense:
        return await self.repository.create_master_license(license_data)