from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.master_love_to import MasterLoveTo
from app.schemas.master_love_to import (
    MasterLoveToCreate,
    MasterLoveToRead,
    MasterLoveToUpdate,  # Assuming you have a MasterLoveToUpdate schema
)


class MasterLoveToRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_valid_ids(self, ids: List[int]) -> List[int]:
        result = await self.db.execute(select(MasterLoveTo.id).where(MasterLoveTo.id.in_(ids)))
        return [row[0] for row in result.fetchall()]

    async def get_master_love_to_by_id(self, love_to_id: int) -> Optional[MasterLoveTo]:
        result = await self.db.execute(select(MasterLoveTo).where(MasterLoveTo.id == love_to_id))
        return result.scalars().first()

    async def get_all_master_love_tos(self) -> List[MasterLoveTo]:
        result = await self.db.execute(select(MasterLoveTo))
        return result.scalars().all()

    async def create_master_love_to(self, love_to_create: MasterLoveToCreate) -> MasterLoveTo:
        love_to = MasterLoveTo(
            label=love_to_create.label,
            # Add other fields if necessary
        )
        self.db.add(love_to)
        try:
            await self.db.commit()
            await self.db.refresh(love_to)
            return love_to
        except IntegrityError:
            await self.db.rollback()
            raise

    async def update_master_love_to(self, love_to_id: int, love_to_update: MasterLoveToUpdate) -> Optional[MasterLoveTo]:
        love_to = await self.get_master_love_to_by_id(love_to_id)
        if not love_to:
            return None
        for field, value in love_to_update.dict(exclude_unset=True).items():
            setattr(love_to, field, value)
        try:
            await self.db.commit()
            await self.db.refresh(love_to)
            return love_to
        except IntegrityError:
            await self.db.rollback()
            raise

    async def delete_master_love_to(self, love_to_id: int) -> bool:
        love_to = await self.get_master_love_to_by_id(love_to_id)
        if not love_to:
            return False
        await self.db.delete(love_to)
        await self.db.commit()
        return True