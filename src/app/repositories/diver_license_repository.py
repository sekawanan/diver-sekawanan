# app/repositories/diver_license_repository.py

from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import DiverLicense  # Ensure this is your SQLAlchemy model
from app.models.dive_preference import DivePreference
from app.models.diver_profile import DiverProfile
from app.schemas.diver_license import DiverLicenseCreate

class DiverLicenseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_diver_profile(self, user_id: str) -> Optional[DiverProfile]:
        result = await self.db.execute(
            select(DiverProfile)
            .options(
                selectinload(DiverProfile.diver_licenses),
                selectinload(DiverProfile.dive_preferences)
                    .selectinload(DivePreference.master_preference),
                selectinload(DiverProfile.diver_gears)
            )
            .where(DiverProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_license(self, diver_profile_id: int, license_data: DiverLicenseCreate) -> DiverLicense:
        new_license = DiverLicense(
            diver_profile_id=diver_profile_id,
            license_institution=license_data.license_institution,
            license_level=license_data.license_level,
            diver_name=license_data.diver_name,
            diver_number=license_data.diver_number,
            birth_date_license=license_data.birth_date_license,
            certificate_date=license_data.certificate_date,
            instructor_name=license_data.instructor_name,
            instructor_number=license_data.instructor_number,
            store_name=license_data.store_name,
            store_number=license_data.store_number
        )
        self.db.add(new_license)
        await self.db.commit()
        await self.db.refresh(new_license)

        result = await self.db.execute(
            select(DiverLicense)
            .where(DiverLicense.diver_profile_id == diver_profile_id)
        )
        return result.scalar_one_or_none()

    async def get_all_licenses_by_diver_profile_id(self, diver_profile_id: int) -> List[DiverLicense]:
        result = await self.db.execute(
            select(DiverLicense)
            .where(DiverLicense.diver_profile_id == diver_profile_id)
        )
        licenses = result.scalars().all()
        return licenses