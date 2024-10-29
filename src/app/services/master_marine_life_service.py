# app/services/master_marine_life_service.py
from typing import List
from app.repositories.master_marine_life_repository import MasterMarineLifeRepository
from app.models.master_marine_life import MasterMarineLife

class MasterMarineLifeService():
    def __init__(self, repository: MasterMarineLifeRepository):
        self.repository = repository
    
    async def get_all_master_marine_lifes(self) -> List[MasterMarineLife]:
        return await self.repository.get_all_master_marine_life()