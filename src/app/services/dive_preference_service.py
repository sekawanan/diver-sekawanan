# app/services/dive_preference_service.py

from typing import List, Optional
from app.repositories.dive_preference_repository import DivePreferenceRepository
from app.schemas.dive_preference import DivePreferenceCreate, DivePreferenceCreateMultiple, DivePreferenceUpdate
from app.models.dive_preference import DivePreference
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import logging

logger = logging.getLogger(__name__)

class DuplicateDivePreferenceError(Exception):
    """Custom exception for duplicate dive preferences."""
    def __init__(self, diver_profile_id: int, master_preference_id: int):
        self.diver_profile_id = diver_profile_id
        self.master_preference_id = master_preference_id
        self.message = f"Diver with profile_id {diver_profile_id} already has master_dive_preference_id {master_preference_id}."
        super().__init__(self.message)

class DivePreferenceService:
    def __init__(self, repository: DivePreferenceRepository):
        self.repository = repository

    async def get_preferences_by_diver(self, diver_profile_id: int) -> List[DivePreference]:
        try:
            preferences = await self.repository.get_preferences_by_diver(diver_profile_id)
            logger.info(f"Retrieved {len(preferences)} dive preferences for diver_profile_id {diver_profile_id}.")
            return preferences
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving dive preferences: {e}")
            raise e

    async def create_preference(self, diver_profile_id: int, preference_data: DivePreferenceCreate) -> DivePreference:
        try:
            # Check if the preference already exists
            existing_preference = await self.repository.get_preference_by_master_id(diver_profile_id, preference_data.master_dive_preference_id)
            if existing_preference:
                logger.warning(f"Dive preference already exists for diver_profile_id {diver_profile_id} and master_preference_id {preference_data.master_dive_preference_id}.")
                raise DuplicateDivePreferenceError(diver_profile_id, preference_data.master_dive_preference_id)
            
            new_preference = await self.repository.create_preference(diver_profile_id, preference_data)
            if not new_preference:
                logger.error("Failed to create dive preference due to IntegrityError.")
                raise Exception("Failed to create dive preference.")
            logger.info(f"Created new dive preference with id {new_preference.id} for diver_profile_id {diver_profile_id}.")
            return new_preference
        except DuplicateDivePreferenceError as e:
            logger.error(e.message)
            raise e
        except IntegrityError as e:
            logger.error(f"IntegrityError during creation: {e}")
            raise e
        except SQLAlchemyError as e:
            logger.error(f"Error creating dive preference: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise e

    async def create_preferences_bulk(self, diver_profile_id: int, preference_data: DivePreferenceCreateMultiple) -> List[DivePreference]:
        created_preferences = []
        try:
            # Fetch existing preferences to avoid duplicates
            existing_preferences = await self.repository.get_preferences_by_diver(diver_profile_id)
            existing_master_ids = {pref.master_dive_preference_id for pref in existing_preferences}
            
            # Filter out duplicates
            unique_master_ids = [pid for pid in preference_data.master_dive_preference_ids if pid not in existing_master_ids]
            
            if not unique_master_ids:
                logger.warning(f"No new dive preferences to create for diver_profile_id {diver_profile_id}. All preferences already exist.")
                return created_preferences  # Empty list
            
            # Call the correct repository method
            new_preferences = await self.repository.create_preferences_bulk(diver_profile_id, unique_master_ids)
            created_preferences.extend(new_preferences)
            
            if len(unique_master_ids) != len(new_preferences):
                logger.warning(f"Some dive preferences could not be created due to duplicates or other issues.")
            
            logger.info(f"Created {len(new_preferences)} new dive preferences for diver_profile_id {diver_profile_id}.")
            return created_preferences
        except IntegrityError as e:
            logger.error(f"IntegrityError during bulk creation: {e}")
            raise DuplicateDivePreferenceError(diver_profile_id, "One or more master_preference_ids") from e
        except SQLAlchemyError as e:
            logger.error(f"Error creating dive preferences in bulk: {e}")
            raise e

    async def update_preference(self, diver_profile_id: int, preference_id: int, preference_update: DivePreferenceUpdate) -> Optional[DivePreference]:
        try:
            # If updating the master_dive_preference_id, ensure it's not creating a duplicate
            if preference_update.master_dive_preference_id is not None:
                existing_preference = await self.repository.get_preference_by_master_id(diver_profile_id, preference_update.master_dive_preference_id)
                if existing_preference and existing_preference.id != preference_id:
                    logger.warning(f"Dive preference already exists for diver_profile_id {diver_profile_id} and master_preference_id {preference_update.master_dive_preference_id}.")
                    raise DuplicateDivePreferenceError(diver_profile_id, preference_update.master_dive_preference_id)
            
            updated_preference = await self.repository.update_preference(diver_profile_id, preference_id, preference_update)
            if updated_preference:
                logger.info(f"Updated dive preference with id {preference_id} for diver_profile_id {diver_profile_id}.")
            else:
                logger.warning(f"Dive preference with id {preference_id} not found for diver_profile_id {diver_profile_id}.")
            return updated_preference
        except DuplicateDivePreferenceError as e:
            logger.error(e.message)
            raise e
        except IntegrityError as e:
            logger.error(f"IntegrityError during update: {e}")
            raise e
        except SQLAlchemyError as e:
            logger.error(f"Error updating dive preference: {e}")
            raise e

    async def delete_preference(self, diver_profile_id: int, preference_id: int) -> bool:
        try:
            success = await self.repository.delete_preference(diver_profile_id, preference_id)
            if success:
                logger.info(f"Deleted dive preference with id {preference_id} for diver_profile_id {diver_profile_id}.")
            else:
                logger.warning(f"Dive preference with id {preference_id} not found for diver_profile_id {diver_profile_id}.")
            return success
        except SQLAlchemyError as e:
            logger.error(f"Error deleting dive preference: {e}")
            raise e