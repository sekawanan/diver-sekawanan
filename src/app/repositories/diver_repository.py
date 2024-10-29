# app/repositories/diver_repository.py
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.diver_profile import DiverProfile

class DiverRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_diver_with_details(self, diver_profile_id: int) -> Optional[DiverProfile]:
        result = await self.db.execute(
            select(DiverProfile)
            .options(selectinload(DiverProfile.licenses))
            .options(selectinload(DiverProfile.dive_preferences).selectinload("master_preference"))
            .where(DiverProfile.id == diver_profile_id)
        )
        diver = result.scalars().first()
        return diver