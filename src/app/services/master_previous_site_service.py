from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.master_previous_dive_site import MasterPreviousDiveSite
from app.schemas.master_previous_dive_site import (
    MasterPreviousDiveSiteCreate,
    MasterPreviousSiteUpdate,
    MasterPreviousDiveSiteRead,
)
from app.repositories.master_previous_dive_site_repository import MasterPreviousDiveSiteRepository

class MasterPreviousSiteService:
    def __init__(self, repository: MasterPreviousDiveSiteRepository):
        self.repository = repository

    async def get_all_master_previous_dive_sites(self) -> List[MasterPreviousDiveSite]:
        return await self.repository.get_all_master_previous_dive_sites()

    async def get_master_previous_dive_site_by_id(self, site_id: int) -> Optional[MasterPreviousDiveSite]:
        return await self.repository.get_master_previous_dive_site_by_id(site_id)

    async def create_master_previous_site(self, site_create: MasterPreviousDiveSiteCreate) -> MasterPreviousDiveSite:
        try:
            return await self.repository.create_master_previous_dive_site(site_create)
        except IntegrityError as e:
            # Log the error as needed
            raise ValueError("Master previous site with this label already exists.") from e

    # async def update_master_previousdive__site(
    #     self, site_id: int, site_update: MasterPreviousDiveSiteUpdate
    # ) -> Optional[MasterPreviousDiveSite]:
    #     try:
    #         return await self.repository.update_master_previous_dive_site(site_id, site_update)
    #     except IntegrityError as e:
    #         # Log the error as needed
    #         raise ValueError("Master previous site with this label already exists.") from e

    async def delete_master_previous_site(self, site_id: int) -> bool:
        return await self.repository.delete_master_previous_dive_site(site_id)