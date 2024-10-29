from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.master_previous_dive_site import MasterPreviousDiveSite
from app.schemas.master_previous_dive_site import (
    MasterPreviousDiveSiteCreate,
    MasterPreviousDiveSiteRead,
    # MasterPreviousDiveSiteUpdate,  # Assuming you have a MasterPreviousSiteUpdate schema
)


class MasterPreviousDiveSiteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_valid_ids(self, ids: List[int]) -> List[int]:
        result = await self.db.execute(select(MasterPreviousDiveSite.id).where(MasterPreviousDiveSite.id.in_(ids)))
        return [row[0] for row in result.fetchall()]

    async def get_master_previous_dive_site_by_id(self, site_id: int) -> Optional[MasterPreviousDiveSite]:
        result = await self.db.execute(select(MasterPreviousDiveSite).where(MasterPreviousDiveSite.id == site_id))
        return result.scalars().first()

    async def get_all_master_previous_dive_sites(self) -> List[MasterPreviousDiveSite]:
        result = await self.db.execute(select(MasterPreviousDiveSite))
        return result.scalars().all()

    async def create_master_previous_dive_site(self, site_create: MasterPreviousDiveSiteCreate) -> MasterPreviousDiveSite:
        site = MasterPreviousDiveSite(
            label=site_create.label,
            # Add other fields if necessary
        )
        self.db.add(site)
        try:
            await self.db.commit()
            await self.db.refresh(site)
            return site
        except IntegrityError:
            await self.db.rollback()
            raise

    # async def update_master_previous_site(self, site_id: int, site_update: MasterPreviousDiveSiteUpdate) -> Optional[MasterPreviousDiveSite]:
    #     site = await self.get_master_previous_site_by_id(site_id)
    #     if not site:
    #         return None
    #     for field, value in site_update.dict(exclude_unset=True).items():
    #         setattr(site, field, value)
    #     try:
    #         await self.db.commit()
    #         await self.db.refresh(site)
    #         return site
    #     except IntegrityError:
    #         await self.db.rollback()
    #         raise

    async def delete_master_previous_dive_site(self, site_id: int) -> bool:
        site = await self.get_master_previous_dive_site_by_id(site_id)
        if not site:
            return False
        await self.db.delete(site)
        await self.db.commit()
        return True