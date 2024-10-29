# app/services/master_dive_site_service.py
from typing import List
from app.repositories.master_dive_site_repository import MasterDiveSiteRepository
from app.models.master_dive_site import MasterDiveSite

class MasterDiveSiteService():
    def __init__(self, repository: MasterDiveSiteRepository):
        self.repository = repository
    
    async def get_all_master_dive_sites(self) -> List[MasterDiveSite]:
        return await self.repository.get_all_master_dive_site()