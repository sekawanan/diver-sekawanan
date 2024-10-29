# app/services/dive_log_service.py

from typing import List, Optional
from app.repositories.dive_log_repository import DiveLogRepository
from app.models.dive_log import DiveLog
from app.schemas.dive_log import DiveLogCreate, DiveLogUpdate


class DiveLogService:
    def __init__(self, repository: DiveLogRepository):
        self.repository = repository

    async def get_all_dive_logs(self) -> List[DiveLog]:
        return await self.repository.get_all()

    async def get_dive_log_by_id(self, dive_log_id: int) -> Optional[DiveLog]:
        return await self.repository.get_by_id(dive_log_id)

    async def create_dive_log(self, dive_log_data: DiveLogCreate) -> DiveLog:
        dive_log = DiveLog(**dive_log_data.dict())
        return await self.repository.create(dive_log)

    async def update_dive_log(
        self, dive_log_id: int, dive_log_data: DiveLogUpdate
    ) -> Optional[DiveLog]:
        dive_log = await self.repository.get_by_id(dive_log_id)
        if not dive_log:
            return None
        updates = dive_log_data.dict(exclude_unset=True)
        return await self.repository.update(dive_log, updates)

    async def delete_dive_log(self, dive_log_id: int) -> bool:
        dive_log = await self.repository.get_by_id(dive_log_id)
        if not dive_log:
            return False
        await self.repository.delete(dive_log)
        return True
