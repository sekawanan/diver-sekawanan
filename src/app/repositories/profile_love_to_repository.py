from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.profile_love_to import ProfileLoveTo
from app.schemas.profile_love_to import (
    ProfileLoveToCreate,
    ProfileLoveToRead,
    ProfileLoveToUpdate,  # Assuming you have a ProfileLoveToUpdate schema
)


class ProfileLoveToRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_profile_love_to_by_id(self, profile_love_to_id: int) -> Optional[ProfileLoveTo]:
        result = await self.db.execute(select(ProfileLoveTo).where(ProfileLoveTo.id == profile_love_to_id))
        return result.scalars().first()

    async def get_all_profile_love_tos(self, skip: int = 0, limit: int = 100) -> List[ProfileLoveTo]:
        result = await self.db.execute(select(ProfileLoveTo).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_profile_love_to(self, profile_love_to_create: ProfileLoveToCreate) -> ProfileLoveTo:
        profile_love_to = ProfileLoveTo(
            onboarding_profile_id=profile_love_to_create.onboarding_profile_id,
            master_love_to_id=profile_love_to_create.master_love_to_id,
            # Add other fields if necessary
        )
        self.db.add(profile_love_to)
        try:
            await self.db.commit()
            await self.db.refresh(profile_love_to)
            return profile_love_to
        except IntegrityError:
            await self.db.rollback()
            raise

    async def update_profile_love_to(self, profile_love_to_id: int, profile_love_to_update: ProfileLoveToUpdate) -> Optional[ProfileLoveTo]:
        profile_love_to = await self.get_profile_love_to_by_id(profile_love_to_id)
        if not profile_love_to:
            return None
        for field, value in profile_love_to_update.dict(exclude_unset=True).items():
            setattr(profile_love_to, field, value)
        try:
            await self.db.commit()
            await self.db.refresh(profile_love_to)
            return profile_love_to
        except IntegrityError:
            await self.db.rollback()
            raise

    async def delete_profile_love_to(self, profile_love_to_id: int) -> bool:
        profile_love_to = await self.get_profile_love_to_by_id(profile_love_to_id)
        if not profile_love_to:
            return False
        await self.db.delete(profile_love_to)
        await self.db.commit()
        return True