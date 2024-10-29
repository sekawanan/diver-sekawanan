from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.profile_previous_dive_site import ProfilePreviousDiveSite
from app.schemas.profile_previous_dive_site import (
    ProfilePreviousDiveSiteCreate,
    ProfilePreviousDiveSiteRead,
    ProfilePreviousDiveSiteUpdate,  # Assuming you have a ProfilePreviousDiveSiteUpdate schema
)


class ProfilePreviousDiveSiteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_profile_previous_dive_site_by_id(self, profile_id: int) -> Optional[ProfilePreviousDiveSite]:
        result = await self.db.execute(select(ProfilePreviousDiveSite).where(ProfilePreviousDiveSite.id == profile_id))
        return result.scalars().first()

    async def get_all_profile_previous_dive_sites(self, skip: int = 0, limit: int = 100) -> List[ProfilePreviousDiveSite]:
        result = await self.db.execute(select(ProfilePreviousDiveSite).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_profile_previous_dive_site(self, profile_previous_dive_site_create: ProfilePreviousDiveSiteCreate) -> ProfilePreviousDiveSite:
        profile_previous_dive_site = ProfilePreviousDiveSite(
            onboarding_profile_id=profile_previous_dive_site_create.onboarding_profile_id,
            master_previous_dive_site_id=profile_previous_dive_site_create.master_previous_dive_site_id,
            # Add other fields if necessary
        )
        self.db.add(profile_previous_dive_site)
        try:
            await self.db.commit()
            await self.db.refresh(profile_previous_dive_site)
            return profile_previous_dive_site
        except IntegrityError:
            await self.db.rollback()
            raise

    async def update_profile_previous_dive_site(self, profile_id: int, profile_previous_dive_site_update: ProfilePreviousDiveSiteUpdate) -> Optional[ProfilePreviousDiveSite]:
        profile_previous_dive_site = await self.get_profile_previous_dive_site_by_id(profile_id)
        if not profile_previous_dive_site:
            return None
        for field, value in profile_previous_dive_site_update.dict(exclude_unset=True).items():
            setattr(profile_previous_dive_site, field, value)
        try:
            await self.db.commit()
            await self.db.refresh(profile_previous_dive_site)
            return profile_previous_dive_site
        except IntegrityError:
            await self.db.rollback()
            raise

    async def delete_profile_previous_dive_site(self, profile_id: int) -> bool:
        profile_previous_dive_site = await self.get_profile_previous_dive_site_by_id(profile_id)
        if not profile_previous_dive_site:
            return False
        await self.db.delete(profile_previous_dive_site)
        await self.db.commit()
        return True