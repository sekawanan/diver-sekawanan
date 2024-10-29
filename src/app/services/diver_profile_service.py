# app/services/diver_profile_service.py
from typing import List, Optional
from app.models.diver_profile import DiverProfile
from app.schemas.diver_profile import DiverProfileCreate, DiverProfileUpdate
from app.repositories.diver_profile_repository import DiverProfileRepository

class DiverProfileService:
    def __init__(self, repository: DiverProfileRepository):
        self.repository = repository

    async def get_all_diver_profiles(self) -> List[DiverProfile]:
        return await self.repository.get_diver_profiles()

    async def get_diver_profile(self, diver_profile_id: int) -> Optional[DiverProfile]:
        return await self.repository.get_diver_profile(diver_profile_id)

    async def create_diver_profile(self, diver_profile: DiverProfileCreate) -> DiverProfile:
        return await self.repository.create_diver_profile(diver_profile)

    async def update_diver_profile(self, diver_profile_id: int, diver_profile: DiverProfileUpdate) -> Optional[DiverProfile]:
        return await self.repository.update_diver_profile(diver_profile_id, diver_profile)

    async def delete_diver_profile(self, diver_profile_id: int) -> bool:
        return await self.repository.delete_diver_profile(diver_profile_id)
