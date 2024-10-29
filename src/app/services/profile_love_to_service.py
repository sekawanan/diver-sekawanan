from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.profile_love_to import ProfileLoveTo
from app.schemas.profile_love_to import (
    ProfileLoveToCreate,
    ProfileLoveToUpdate,
    ProfileLoveToRead,
)
from app.repositories.profile_love_to_repository import ProfileLoveToRepository

class ProfileLoveToService:
    def __init__(self, repository: ProfileLoveToRepository):
        self.repository = repository

    async def get_all_profile_love_tos(self) -> List[ProfileLoveTo]:
        return await self.repository.get_all_profile_love_tos()

    async def get_profile_love_to_by_id(self, love_to_id: int) -> Optional[ProfileLoveTo]:
        return await self.repository.get_profile_love_to_by_id(love_to_id)

    async def create_profile_love_to(self, love_to_create: ProfileLoveToCreate) -> ProfileLoveTo:
        try:
            return await self.repository.create_profile_love_to(love_to_create)
        except IntegrityError as e:
            # Log the error as needed
            raise ValueError("Profile love to with these IDs already exists.") from e

    async def update_profile_love_to(
        self, love_to_id: int, love_to_update: ProfileLoveToUpdate
    ) -> Optional[ProfileLoveTo]:
        try:
            return await self.repository.update_profile_love_to(love_to_id, love_to_update)
        except IntegrityError as e:
            # Log the error as needed
            raise ValueError("Profile love to with these IDs already exists.") from e

    async def delete_profile_love_to(self, love_to_id: int) -> bool:
        return await self.repository.delete_profile_love_to(love_to_id)