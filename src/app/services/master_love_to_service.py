from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.master_love_to import MasterLoveTo
from app.schemas.master_love_to import (
    MasterLoveToCreate,
    MasterLoveToUpdate,
    MasterLoveToRead,
)
from app.repositories.master_love_to_repository import MasterLoveToRepository

class MasterLoveToService:
    def __init__(self, master_love_to_repository: MasterLoveToRepository):
        self.master_love_to_repository = master_love_to_repository

    async def get_all_master_love_tos(self) -> List[MasterLoveTo]:
        return await self.master_love_to_repository.get_all_master_love_tos()

    async def get_master_love_to_by_id(self, love_to_id: int) -> Optional[MasterLoveTo]:
        return await self.master_love_to_repository.get_master_love_to_by_id(love_to_id)

    async def create_master_love_to(self, love_to_create: MasterLoveToCreate) -> MasterLoveTo:
        try:
            return await self.master_love_to_repository.create_master_love_to(love_to_create)
        except IntegrityError as e:
            # Log the error as needed
            raise ValueError("Master love to with this label already exists.") from e

    async def update_master_love_to(
        self, love_to_id: int, love_to_update: MasterLoveToUpdate
    ) -> Optional[MasterLoveTo]:
        try:
            return await self.master_love_to_repository.update_master_love_to(love_to_id, love_to_update)
        except IntegrityError as e:
            # Log the error as needed
            raise ValueError("Master love to with this label already exists.") from e

    async def delete_master_love_to(self, love_to_id: int) -> bool:
        return await self.master_love_to_repository.delete_master_love_to(love_to_id)