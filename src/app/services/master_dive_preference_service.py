# app/services/master_dive_preference_service.py
from typing import List
from app.repositories.master_dive_preference_repository import MasterDivePreferenceRepository
from app.models.master_dive_preference import MasterDivePreference

class MasterDivePreferenceService:
    def __init__(self, repository: MasterDivePreferenceRepository):
        self.repository = repository

    async def get_all_master_dive_preferences(self) -> List[MasterDivePreference]:
        return await self.repository.get_all_master_dive_preferences()

    async def create_master_dive_preference(self, preference_data: MasterDivePreference) -> MasterDivePreference:
        return await self.repository.create_master_dive_preference(preference_data)