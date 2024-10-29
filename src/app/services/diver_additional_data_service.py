# app/services/diver_additional_data_service.py
from typing import List

from app.models.diver_additional_data import DiverAdditionalData
from app.repositories.diver_additional_data_repository import DiverAdditionalDataRepository

class DiverAdditionalDataService:
    def __init__(self, repository: DiverAdditionalDataRepository):
        self.repository = repository
    
    async def get_all_diver_additional_data(self) -> List[DiverAdditionalData]:
        return await self.repository.get_diver_additional_data()
