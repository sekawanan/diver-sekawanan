# app/services/dive_type_service.py

from typing import List, Optional
from app.repositories.master_dive_type_repository import MasterDiveTypeRepository
from app.models.master_dive_type import MasterDiveType
from app.schemas.master_dive_type import MasterDiveTypeUpdate, MasterDiveTypeCreate

class MasterDiveTypeService:
    def __init__(self, repository: MasterDiveTypeRepository):
        self.repository = repository

    async def get_all_dive_types(self) -> List[MasterDiveType]:
        return await self.repository.get_all()

    async def get_dive_type_by_id(self, dive_type_id: int) -> Optional[MasterDiveType]:
        return await self.repository.get_by_id(dive_type_id)

    async def create_dive_type(self, dive_type_data: MasterDiveTypeCreate) -> MasterDiveType:
        dive_type = MasterDiveType(**dive_type_data.dict())
        return await self.repository.create(dive_type)

    async def update_dive_type(
        self, dive_type_id: int, dive_type_data: MasterDiveTypeUpdate
    ) -> Optional[MasterDiveType]:
        dive_type = await self.repository.get_by_id(dive_type_id)
        if not dive_type:
            return None
        updates = dive_type_data.dict(exclude_unset=True)
        return await self.repository.update(dive_type, updates)

    async def delete_dive_type(self, dive_type_id: int) -> bool:
        dive_type = await self.repository.get_by_id(dive_type_id)
        if not dive_type:
            return False
        await self.repository.delete(dive_type)
        return True
