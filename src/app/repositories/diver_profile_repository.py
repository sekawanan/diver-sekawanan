# app/repositories/diver_profile_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from sqlalchemy.orm import selectinload

from app.models.diver_profile import DiverProfile
from app.schemas.diver_profile import DiverProfileCreate, DiverProfileUpdate
from app.models.dive_preference import DivePreference
from app.models.diver_license import DiverLicense
from app.models.master_gear import MasterGear
from app.models.master_brand import MasterBrand
from app.models.master_gear_brand import MasterGearBrand
from app.models.diver_gear import DiverGear

class DiverProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_diver_profiles(self) -> List[DiverProfile]:
        result = await self.db.execute(
            select(DiverProfile)
            .options(
                selectinload(DiverProfile.diver_licenses)
                    .selectinload(DiverLicense.master_license),
                selectinload(DiverProfile.dive_preferences)
                    .selectinload(DivePreference.master_preference),
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_color),
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_gears_brand)
                        .selectinload(MasterGearBrand.master_gear),
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_gears_brand)
                        .selectinload(MasterGearBrand.master_brand),
            )
        )
        return result.scalars().all()

    async def get_diver_profile(self, diver_profile_id: int) -> Optional[DiverProfile]:
        result = await self.db.execute(
            select(DiverProfile)
            .options(
                selectinload(DiverProfile.diver_licenses)
                    .selectinload(DiverLicense.master_license),
                selectinload(DiverProfile.dive_preferences)
                    .selectinload(DivePreference.master_preference),
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_color),
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_gears_brand)
                        .selectinload(MasterGearBrand.master_gear),
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_gears_brand)
                        .selectinload(MasterGearBrand.master_brand),
            )
            .where(DiverProfile.id == diver_profile_id)
        )
        return result.scalar_one_or_none()
    
    async def get_diver_profile_by_id(self, diver_profile_id: int) -> Optional[DiverProfile]:
        result = await self.db.execute(
            select(DiverProfile)
            .where(DiverProfile.id == diver_profile_id)
            .options(
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_color),
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_gears_brand)
                        .selectinload(MasterGearBrand.master_brand),
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_gears_brand)
                        .selectinload(MasterGearBrand.master_gear),
                selectinload(DiverProfile.diver_licenses)
                    .selectinload(DiverLicense.master_license),
                selectinload(DiverProfile.dive_preferences)
                    .selectinload(DivePreference.master_preference),
            )
        )
        return result.scalars().first()

    async def create_diver_profile(self, diver_profile: DiverProfileCreate) -> DiverProfile:
        db_diver_profile = DiverProfile(**diver_profile.dict())
        self.db.add(db_diver_profile)
        await self.db.commit()
        await self.db.refresh(db_diver_profile)

        # Ensure relationships are loaded
        result = await self.db.execute(
            select(DiverProfile)
            .options(
                selectinload(DiverProfile.diver_licenses)
                    .selectinload(DiverLicense.master_license),
                selectinload(DiverProfile.dive_preferences)
                    .selectinload(DivePreference.master_preference),
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_color),
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_gears_brand)
                        .selectinload(MasterGearBrand.master_gear),
                selectinload(DiverProfile.diver_gears)
                    .selectinload(DiverGear.master_gears_brand)
                        .selectinload(MasterGearBrand.master_brand),
            )
            .where(DiverProfile.id == db_diver_profile.id)
        )
        return result.scalar_one()

    async def update_diver_profile(self, diver_profile_id: int, diver_profile: DiverProfileUpdate) -> Optional[DiverProfile]:
        db_diver_profile = await self.get_diver_profile(diver_profile_id)
        if not db_diver_profile:
            return None
        for var, value in vars(diver_profile).items():
            if value is not None:
                setattr(db_diver_profile, var, value)
        self.db.add(db_diver_profile)
        await self.db.commit()
        await self.db.refresh(db_diver_profile)
        return db_diver_profile

    async def delete_diver_profile(self, diver_profile_id: int) -> bool:
        db_diver_profile = await self.get_diver_profile(diver_profile_id)
        if not db_diver_profile:
            return False
        await self.db.delete(db_diver_profile)
        await self.db.commit()
        return True