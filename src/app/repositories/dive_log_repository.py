# app/repositories/dive_log_repository.py

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.dive_log import DiveLog


class DiveLogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[DiveLog]:
        result = await self.db.execute(
            select(DiveLog)
            .options(
                selectinload(DiveLog.diver_profile),
                selectinload(DiveLog.master_dive_site),
                selectinload(DiveLog.master_dive_type)
                # Add other relationships if needed
            )
        )
        return result.scalars().all()

    async def get_by_id(self, dive_log_id: int) -> Optional[DiveLog]:
        result = await self.db.execute(
            select(DiveLog)
            .options(
                selectinload(DiveLog.diver_profile),
                selectinload(DiveLog.master_dive_site),
                # Add other relationships if needed
            )
            .where(DiveLog.id == dive_log_id)
        )
        return result.scalar_one_or_none()

    async def create(self, dive_log: DiveLog) -> DiveLog:
        self.db.add(dive_log)
        await self.db.commit()
        await self.db.refresh(dive_log)
        return dive_log

    async def update(self, dive_log: DiveLog, updates: dict) -> DiveLog:
        for key, value in updates.items():
            setattr(dive_log, key, value)
        self.db.add(dive_log)
        await self.db.commit()
        await self.db.refresh(dive_log)
        return dive_log

    async def delete(self, dive_log: DiveLog) -> None:
        await self.db.delete(dive_log)
        await self.db.commit()
