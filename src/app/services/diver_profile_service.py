# app/services/diver_profile_service.py
from typing import List, Optional
from app.models.diver_profile import DiverProfile
from app.schemas.diver_profile import DiverProfileCreate, DiverProfileRead, DiverProfileUpdate, DiverProfileUpdateProfilePicture
from app.repositories.diver_profile_repository import DiverProfileRepository

class DiverProfileService:
    def __init__(self, repository: DiverProfileRepository):
        self.repository = repository

    async def get_all_diver_profiles(self) -> List[DiverProfile]:
        return await self.repository.get_diver_profiles()

    async def get_diver_profile(self, user_id: str) -> Optional[DiverProfile]:
        fetched_profile = await self.repository.get_diver_profile(user_id)
        return DiverProfileRead.from_orm(fetched_profile)

    async def create_diver_profile(self, user_id: str, diver_profile: DiverProfileCreate) -> DiverProfile:
        created_profile = await self.repository.create_diver_profile(user_id, diver_profile)
        return DiverProfileRead.from_orm(created_profile)

    async def update_diver_profile(self, user_id: str, diver_profile: DiverProfileUpdate) -> Optional[DiverProfile]:
        await self.repository.update_diver_profile(user_id, diver_profile)
        fetched_profile = await self.repository.get_diver_profile(user_id)
        return DiverProfileRead.from_orm(fetched_profile)
    
    async def add_diver_profile_picture(self, user_id: str, diver_profile: DiverProfileUpdateProfilePicture) -> Optional[DiverProfile]:
        await self.repository.update_diver_profile_picture(user_id, diver_profile)
        fetched_profile = await self.repository.get_diver_profile(user_id)
        return DiverProfileRead.from_orm(fetched_profile)

    async def delete_diver_profile(self, user_id: str) -> bool:
        return await self.repository.delete_diver_profile(user_id)
