# app/services/master_color_service.py
from typing import List
from app.repositories.master_color_repository import MasterColorRepository
from app.models.master_color import MasterColor

class MasterColorService():
    def __init__(self, repository: MasterColorRepository):
        self.repository = repository
    
    async def get_all_master_colors(self) -> List[MasterColor]:
        return await self.repository.get_all_master_color()