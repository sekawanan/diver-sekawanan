# app/repositories/onboarding_profile_repository.py

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
import uuid

from app.models.onboarding_profile import OnboardingProfile
from app.schemas.onboarding_profile import (
    OnboardingProfileCreate,
    OnboardingProfileRead,
    OnboardingProfileUpdate,
)
from app.models.profile_love_to import ProfileLoveTo
from app.models.profile_previous_dive_site import ProfilePreviousDiveSite
from app.schemas.onboarding_profile import OnboardingProfileCreateRequest

class OnboardingProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_onboarding_profile_by_id(self, profile_id: int) -> Optional[OnboardingProfile]:
        result = await self.db.execute(
            select(OnboardingProfile)
            .options(
                selectinload(OnboardingProfile.profile_love_tos)
                .selectinload(ProfileLoveTo.master_love_to),
                selectinload(OnboardingProfile.profile_previous_dive_sites)
                .selectinload(ProfilePreviousDiveSite.master_previous_dive_site)
            )
            .where(OnboardingProfile.id == profile_id)
        )
        return result.scalars().first()
    
    async def get_onboarding_profile_by_user_id(self, user_id: str) -> Optional[OnboardingProfile]:
        result = await self.db.execute(
            select(OnboardingProfile)
            .options(
                selectinload(OnboardingProfile.profile_love_tos)
                .selectinload(ProfileLoveTo.master_love_to),
                selectinload(OnboardingProfile.profile_previous_dive_sites)
                .selectinload(ProfilePreviousDiveSite.master_previous_dive_site)
            )
            .where(OnboardingProfile.user_id == user_id)
        )
        return result.scalars().first()

    async def get_all_onboarding_profiles(self, skip: int = 0, limit: int = 100) -> List[OnboardingProfile]:
        result = await self.db.execute(
            select(OnboardingProfile)
            .options(
                selectinload(OnboardingProfile.profile_love_tos)
                .selectinload(ProfileLoveTo.master_love_to),
                selectinload(OnboardingProfile.profile_previous_dive_sites)
                .selectinload(ProfilePreviousDiveSite.master_previous_dive_site)
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_onboarding_profile(
        self, profile_data: OnboardingProfileCreateRequest, user_id: str
    ) -> OnboardingProfile:
        onboarding_profile = OnboardingProfile(
            user_id=user_id,
            gender=profile_data.gender,
            start_diving=profile_data.start_diving,
            last_time_diving=profile_data.last_time_diving,
            current_logs=profile_data.current_logs,
            last_certification=profile_data.last_certification,
            certification_issuer=profile_data.certification_issuer,
            want_to_see=profile_data.want_to_see,
            dive_current_condition=profile_data.dive_current_condition,
            bottom_time=profile_data.bottom_time,
            trouble_equalizing=profile_data.trouble_equalizing,
            photographer=profile_data.photographer,
            information=profile_data.information
        )
        self.db.add(onboarding_profile)
        await self.db.flush()  # Persist the profile to get its ID
        # Note: Do not refresh here; we will fetch with relations later
        return onboarding_profile

    async def create_profile_love_tos(
        self, onboarding_profile_id: int, master_love_to_ids: List[int]
    ) -> List[ProfileLoveTo]:
        profile_love_tos = [
            ProfileLoveTo(onboarding_profile_id=onboarding_profile_id, master_love_to_id=mid)
            for mid in master_love_to_ids
        ]
        self.db.add_all(profile_love_tos)
        return profile_love_tos

    async def create_profile_previous_dive_sites(
        self, onboarding_profile_id: int, master_previous_dive_site_ids: List[int]
    ) -> List[ProfilePreviousDiveSite]:
        profile_previous_dive_sites = [
            ProfilePreviousDiveSite(onboarding_profile_id=onboarding_profile_id, master_previous_dive_site_id=mid)
            for mid in master_previous_dive_site_ids
        ]
        self.db.add_all(profile_previous_dive_sites)
        return profile_previous_dive_sites

    async def update_onboarding_profile(self, profile_id: int, profile_update: OnboardingProfileUpdate) -> Optional[OnboardingProfile]:
        profile = await self.get_onboarding_profile_by_id(profile_id)
        if not profile:
            return None
        for field, value in profile_update.dict(exclude_unset=True).items():
            setattr(profile, field, value)
        try:
            await self.db.commit()
            await self.db.refresh(profile)
            return profile
        except IntegrityError:
            await self.db.rollback()
            raise

    async def delete_onboarding_profile(self, profile_id: int) -> bool:
        profile = await self.get_onboarding_profile_by_id(profile_id)
        if not profile:
            return False
        await self.db.delete(profile)
        await self.db.commit()
        return True
    
    # New Methods for Synchronizing Associations
    async def synchronize_profile_love_tos(
        self, profile: OnboardingProfile, master_love_to_ids: List[int]
    ) -> None:
        existing_ids = {plt.master_love_to_id for plt in profile.profile_love_tos}
        new_ids = set(master_love_to_ids)

        # Determine IDs to add and remove
        to_add = new_ids - existing_ids
        to_remove = existing_ids - new_ids

        # Add new associations
        for mid in to_add:
            new_plt = ProfileLoveTo(onboarding_profile_id=profile.id, master_love_to_id=mid)
            self.db.add(new_plt)

        # Remove obsolete associations
        if to_remove:
            await self.db.execute(
                ProfileLoveTo.__table__.delete().where(
                    ProfileLoveTo.onboarding_profile_id == profile.id,
                    ProfileLoveTo.master_love_to_id.in_(to_remove)
                )
            )

    async def synchronize_profile_previous_dive_sites(
        self, profile: OnboardingProfile, master_previous_dive_site_ids: List[int]
    ) -> None:
        existing_ids = {ppds.master_previous_dive_site_id for ppds in profile.profile_previous_dive_sites}
        new_ids = set(master_previous_dive_site_ids)

        # Determine IDs to add and remove
        to_add = new_ids - existing_ids
        to_remove = existing_ids - new_ids

        # Add new associations
        for mid in to_add:
            new_ppds = ProfilePreviousDiveSite(onboarding_profile_id=profile.id, master_previous_dive_site_id=mid)
            self.db.add(new_ppds)

        # Remove obsolete associations
        if to_remove:
            await self.db.execute(
                ProfilePreviousDiveSite.__table__.delete().where(
                    ProfilePreviousDiveSite.onboarding_profile_id == profile.id,
                    ProfilePreviousDiveSite.master_previous_dive_site_id.in_(to_remove)
                )
            )