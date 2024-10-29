from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.profile_previous_dive_site import ProfilePreviousDiveSite
from app.schemas.profile_previous_dive_site import (
    ProfilePreviousDiveSiteCreate,
    ProfilePreviousDiveSiteUpdate,
    ProfilePreviousDiveSiteRead,
)
from app.repositories.profile_previous_dive_site_repository import ProfilePreviousDiveSiteRepository

class ProfilePreviousDiveSiteService:
    def __init__(self, repository: ProfilePreviousDiveSiteRepository):
        self.repository = repository

    async def get_all_profile_previous_dive_sites(self) -> List[ProfilePreviousDiveSite]:
        return await self.repository.get_all_profile_previous_dive_sites()

    async def get_profile_previous_dive_site_by_id(self, dive_site_id: int) -> Optional[ProfilePreviousDiveSite]:
        return await self.repository.get_profile_previous_dive_site_by_id(dive_site_id)

    async def create_profile_previous_dive_site(
        self, dive_site_create: ProfilePreviousDiveSiteCreate
    ) -> ProfilePreviousDiveSite:
        try:
            return await self.repository.create_profile_previous_dive_site(dive_site_create)
        except IntegrityError as e:
            # Log the error as needed
            raise ValueError("Profile previous dive site with these IDs already exists.") from e

    async def update_profile_previous_dive_site(
        self, dive_site_id: int, dive_site_update: ProfilePreviousDiveSiteUpdate
    ) -> Optional[ProfilePreviousDiveSite]:
        try:
            return await self.repository.update_profile_previous_dive_site(dive_site_id, dive_site_update)
        except IntegrityError as e:
            # Log the error as needed
            raise ValueError("Profile previous dive site with these IDs already exists.") from e

    async def delete_profile_previous_dive_site(self, dive_site_id: int) -> bool:
        return await self.repository.delete_profile_previous_dive_site(dive_site_id)