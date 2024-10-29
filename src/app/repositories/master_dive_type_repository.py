# app/repositories/msaster_dive_type_repository.py

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.master_dive_type import MasterDiveType

class MasterDiveTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[MasterDiveType]:
        result = await self.db.execute(select(MasterDiveType))
        return result.scalars().all()

    async def get_by_id(self, dive_type_id: int) -> Optional[MasterDiveType]:
        result = await self.db.execute(
            select(MasterDiveType)
            .where(MasterDiveType.id == dive_type_id)
        )
        return result.scalar_one_or_none()

    async def create(self, dive_type: MasterDiveType) -> MasterDiveType:
        self.db.add(dive_type)
        await self.db.commit()
        await self.db.refresh(dive_type)
        return dive_type

    async def update(self, dive_type: MasterDiveType, updates: dict) -> MasterDiveType:
        for key, value in updates.items():
            setattr(dive_type, key, value)
        self.db.add(dive_type)
        await self.db.commit()
        await self.db.refresh(dive_type)
        return dive_type

    async def delete(self, dive_type: MasterDiveType) -> None:
        await self.db.delete(dive_type)
        await self.db.commit()