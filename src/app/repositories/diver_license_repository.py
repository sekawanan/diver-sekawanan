# app/repositories/diver_license_repository.py

from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import DiverLicense  # Ensure this is your SQLAlchemy model
from app.schemas.diver_license import DiverLicenseCreate, DiverLicenseUpdate

class DiverLicenseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_license(self, diver_profile_id: int, license_data: DiverLicenseCreate) -> DiverLicense:
        new_license = DiverLicense(
            diver_profile_id=diver_profile_id,
            master_license_id=license_data.master_license_id,
            certification_number=license_data.certification_number,
            certificate_date=license_data.certificate_date,
            birth_date_license=license_data.birth_date_license,
            instructor_name=license_data.instructor_name,
            instructor_number=license_data.instructor_number,
            store_name=license_data.store_name,
            store_number=license_data.store_number
        )
        self.db.add(new_license)
        await self.db.commit()
        await self.db.refresh(new_license)
        return new_license

    async def get_all_licenses(self) -> List[DiverLicense]:
        result = await self.db.execute(
            select(DiverLicense).options(selectinload(DiverLicense.master_license))
        )
        licenses = result.scalars().all()
        return licenses

    async def get_license_by_id(self, license_id: int) -> Optional[DiverLicense]:
        result = await self.db.execute(
            select(DiverLicense).options(selectinload(DiverLicense.master_license)).where(DiverLicense.id == license_id)
        )
        license = result.scalar_one_or_none()
        return license

    async def get_licenses_by_profile_id(self, diver_profile_id: int) -> List[DiverLicense]:
        result = await self.db.execute(
            select(DiverLicense).options(selectinload(DiverLicense.master_license)).where(DiverLicense.diver_profile_id == diver_profile_id)
        )
        licenses = result.scalars().all()
        return licenses

    async def get_latest_license_by_profile_id(self, diver_profile_id: int) -> Optional[DiverLicense]:
        result = await self.db.execute(
            select(DiverLicense)
            .options(selectinload(DiverLicense.master_license))
            .where(DiverLicense.diver_profile_id == diver_profile_id)
            .order_by(DiverLicense.certificate_date.desc())
            .limit(1)
        )
        latest_license = result.scalar_one_or_none()
        return latest_license

    async def update_license(self, license_id: int, license_update: DiverLicenseUpdate) -> Optional[DiverLicense]:
        license = await self.get_license_by_id(license_id)
        if not license:
            return None

        for var, value in vars(license_update).items():
            if value is not None:
                setattr(license, var, value)

        self.db.add(license)
        await self.db.commit()
        await self.db.refresh(license)
        return license

    async def delete_license(self, license_id: int) -> bool:
        license = await self.get_license_by_id(license_id)
        if not license:
            return False
        await self.db.delete(license)
        await self.db.commit()
        return True