# app/repositories/dive_preference_repository.py

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.models.dive_preference import DivePreference
from app.schemas.dive_preference import DivePreferenceCreate, DivePreferenceUpdate

import logging  # Import logging

# Configure logger
logger = logging.getLogger(__name__)

class DivePreferenceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_preferences_by_diver(self, diver_profile_id: int) -> List[DivePreference]:
        result = await self.db.execute(
            select(DivePreference)
            .options(selectinload(DivePreference.master_preference))
            .where(DivePreference.diver_profile_id == diver_profile_id)
        )
        preferences = result.scalars().all()
        return preferences

    async def get_preference_by_id(self, diver_profile_id: int, preference_id: int) -> Optional[DivePreference]:
        result = await self.db.execute(
            select(DivePreference)
            .options(selectinload(DivePreference.master_preference))
            .where(
                DivePreference.diver_profile_id == diver_profile_id,
                DivePreference.id == preference_id
            )
        )
        preference = result.scalar_one_or_none()
        return preference

    async def get_preference_by_master_id(self, diver_profile_id: int, master_preference_id: int) -> Optional[DivePreference]:
        result = await self.db.execute(
            select(DivePreference)
            .where(
                DivePreference.diver_profile_id == diver_profile_id,
                DivePreference.master_dive_preference_id == master_preference_id
            )
        )
        preference = result.scalar_one_or_none()
        return preference

    async def create_preference(self, diver_profile_id: int, preference_data: DivePreferenceCreate) -> Optional[DivePreference]:
        new_preference = DivePreference(
            diver_profile_id=diver_profile_id,
            master_dive_preference_id=preference_data.master_dive_preference_id
        )
        self.db.add(new_preference)
        try:
            await self.db.commit()
            await self.db.refresh(new_preference)
            # Eagerly load the master_preference
            result = await self.db.execute(
                select(DivePreference)
                .options(selectinload(DivePreference.master_preference))
                .where(DivePreference.id == new_preference.id)
            )
            new_preference = result.scalar_one()
            return new_preference
        except IntegrityError:
            await self.db.rollback()
            logger.error("IntegrityError: Foreign key constraint failed during single preference creation.")
            return None  # Handle this case in the service layer

    async def create_preferences_bulk(self, diver_profile_id: int, preference_ids: List[int]) -> List[DivePreference]:
        """
        Creates multiple DivePreference entries in bulk.

        :param diver_profile_id: ID of the diver profile.
        :param preference_ids: List of master dive preference IDs to associate with the diver.
        :return: List of successfully created DivePreference objects with 'master_preference' loaded.
        """
        new_preferences = [
            DivePreference(
                diver_profile_id=diver_profile_id,
                master_dive_preference_id=pid
            )
            for pid in preference_ids
        ]
        self.db.add_all(new_preferences)
        
        try:
            await self.db.commit()
            for pref in new_preferences:
                await self.db.refresh(pref)
                
            # Eagerly load the 'master_preference' for the newly created preferences
            result = await self.db.execute(
                select(DivePreference)
                .options(selectinload(DivePreference.master_preference))  # Eagerly load the relationship
                .where(DivePreference.diver_profile_id == diver_profile_id)
            )
            created_preferences = result.scalars().all()
            return created_preferences

        except Exception as e:
            await self.db.rollback()
            raise e

    async def update_preference(self, diver_profile_id: int, preference_id: int, preference_update: DivePreferenceUpdate) -> Optional[DivePreference]:
        preference = await self.get_preference_by_id(diver_profile_id, preference_id)
        if not preference:
            return None

        update_data = preference_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(preference, key, value)

        self.db.add(preference)
        try:
            await self.db.commit()
            await self.db.refresh(preference)
            # Eagerly load the master_preference
            result = await self.db.execute(
                select(DivePreference)
                .options(selectinload(DivePreference.master_preference))
                .where(DivePreference.id == preference.id)
            )
            updated_preference = result.scalar_one()
            return updated_preference
        except IntegrityError:
            await self.db.rollback()
            logger.error("IntegrityError: Foreign key constraint failed during preference update.")
            return None  # Handle this case in the service layer

    async def delete_preference(self, diver_profile_id: int, preference_id: int) -> bool:
        preference = await self.get_preference_by_id(diver_profile_id, preference_id)
        if not preference:
            return False
        await self.db.delete(preference)
        try:
            await self.db.commit()
            logger.info(f"Deleted DivePreference with id {preference_id} for diver_profile_id {diver_profile_id}.")
            return True
        except IntegrityError:
            await self.db.rollback()
            logger.error("IntegrityError: Foreign key constraint failed during preference deletion.")
            return False