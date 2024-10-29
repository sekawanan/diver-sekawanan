# app/repositories.diver_additional_data_repository.py
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.diver_additional_data import DiverAdditionalData
from app.models.diver_profile import DiverProfile

class DiverAdditionalDataRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_diver_additional_data(self) -> List[DiverAdditionalData]:
        result = await self.db.execute(select(DiverAdditionalData))
        return result.scalars().all