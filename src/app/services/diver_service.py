# app/services/diver_service.py
from typing import Optional
from app.repositories.diver_repository import DiverRepository
from app.models.diver_profile import DiverProfile

class DiverService:
    def __init__(self, repository: DiverRepository):
        self.repository = repository

    async def get_diver_info(self, diver_profile_id: int) -> Optional[DiverProfile]:
        return await self.repository.get_diver_with_details(diver_profile_id)