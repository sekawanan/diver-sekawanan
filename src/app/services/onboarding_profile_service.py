# app/services/onboarding_profile_service.py

from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.models.onboarding_profile import OnboardingProfile
from app.schemas.onboarding_profile import (
    OnboardingProfileCreate,
    OnboardingProfileUpdate,
    OnboardingProfileRead,
    OnboardingProfileWithRelations
)
from app.repositories.onboarding_profile_repository import OnboardingProfileRepository
from app.repositories.master_love_to_repository import MasterLoveToRepository
from app.repositories.master_previous_dive_site_repository import MasterPreviousDiveSiteRepository
from app.schemas.onboarding_profile import OnboardingProfileCreateRequest
import logging

logger = logging.getLogger(__name__)

class OnboardingProfileService:
    def __init__(
        self,
        onboarding_profile_repository: OnboardingProfileRepository,
        master_love_to_repository: MasterLoveToRepository,
        master_previous_dive_site_repository: MasterPreviousDiveSiteRepository
    ):
        self.onboarding_profile_repository = onboarding_profile_repository
        self.master_love_to_repository = master_love_to_repository
        self.master_previous_dive_site_repository = master_previous_dive_site_repository

    async def get_all_onboarding_profiles(self, skip: int = 0, limit: int = 100) -> List[OnboardingProfileWithRelations]:
        profiles = await self.onboarding_profile_repository.get_all_onboarding_profiles(skip=skip, limit=limit)
        return [OnboardingProfileWithRelations.from_orm(profile) for profile in profiles]

    async def get_onboarding_profile_by_id(self, profile_id: int) -> Optional[OnboardingProfileWithRelations]:
        profile = await self.onboarding_profile_repository.get_onboarding_profile_by_id(profile_id)
        if profile:
            return OnboardingProfileWithRelations.from_orm(profile)
        return None

    async def create_onboarding_profile(
        self, profile_create: OnboardingProfileCreate
    ) -> OnboardingProfile:
        try:
            return await self.onboarding_profile_repository.create_onboarding_profile(profile_create)
        except IntegrityError as e:
            logger.exception("IntegrityError occurred while creating onboarding profile.")
            raise HTTPException(
                status_code=400,
                detail="Onboarding profile with these details already exists."
            ) from e

    async def create_onboarding_profile_with_associations(
        self, profile_data: OnboardingProfileCreateRequest
    ) -> OnboardingProfileWithRelations:
        try:
            # Check if a profile already exists for the given user_id
            existing_profile = await self.onboarding_profile_repository.get_onboarding_profile_by_user_id(profile_data.user_id)
            if existing_profile:
                logger.warning(f"Attempted to create duplicate onboarding profile for user_id: {profile_data.user_id}")
                raise HTTPException(
                    status_code=409,
                    detail="Onboarding profile for this user_id already exists."
                )

            # Validate Master Love To IDs
            valid_love_to_ids = await self.master_love_to_repository.get_valid_ids(profile_data.master_love_to_ids)
            invalid_love_to_ids = set(profile_data.master_love_to_ids) - set(valid_love_to_ids)
            if invalid_love_to_ids:
                logger.warning(f"Invalid Master Love To IDs: {sorted(invalid_love_to_ids)}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid Master Love To IDs: {sorted(invalid_love_to_ids)}"
                )

            # Validate Master Previous Dive Site IDs
            valid_previous_site_ids = await self.master_previous_dive_site_repository.get_valid_ids(profile_data.master_previous_dive_site_ids)
            invalid_previous_site_ids = set(profile_data.master_previous_dive_site_ids) - set(valid_previous_site_ids)
            if invalid_previous_site_ids:
                logger.warning(f"Invalid Master Previous Dive Site IDs: {sorted(invalid_previous_site_ids)}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid Master Previous Dive Site IDs: {sorted(invalid_previous_site_ids)}"
                )

            # Create the onboarding profile
            onboarding_profile = await self.onboarding_profile_repository.create_onboarding_profile(profile_data)
            
            # Create profile love tos if any
            if profile_data.master_love_to_ids:
                await self.onboarding_profile_repository.create_profile_love_tos(
                    onboarding_profile_id=onboarding_profile.id,
                    master_love_to_ids=profile_data.master_love_to_ids
                )
            
            # Create profile previous dive sites if any
            if profile_data.master_previous_dive_site_ids:
                await self.onboarding_profile_repository.create_profile_previous_dive_sites(
                    onboarding_profile_id=onboarding_profile.id,
                    master_previous_dive_site_ids=profile_data.master_previous_dive_site_ids
                )

            # After operations, fetch the profile with relations
            created_profile = await self.onboarding_profile_repository.get_onboarding_profile_by_id(onboarding_profile.id)
            if not created_profile:
                logger.error(f"Failed to retrieve the created onboarding profile with ID: {onboarding_profile.id}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to retrieve the created onboarding profile."
                )
            logger.info(f"Created onboarding profile with ID: {created_profile.id}")
            return OnboardingProfileWithRelations.from_orm(created_profile)
        except IntegrityError as e:
            logger.exception("IntegrityError occurred while creating onboarding profile with associations.")
            raise HTTPException(status_code=400, detail="Integrity error occurred.")
        except HTTPException as he:
            logger.error(f"HTTPException occurred: {he.detail}")
            raise he
        except Exception as e:
            logger.exception("Unexpected error occurred while creating onboarding profile with associations.")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def update_onboarding_profile(
        self, profile_id: int, profile_update: OnboardingProfileUpdate
    ) -> Optional[OnboardingProfileWithRelations]:
        try:
            # Fetch existing profile
            profile = await self.onboarding_profile_repository.get_onboarding_profile_by_id(profile_id)
            if not profile:
                logger.warning(f"Onboarding profile with ID {profile_id} not found for update.")
                raise HTTPException(
                    status_code=404,
                    detail="Onboarding profile not found."
                )

            # If user_id is being updated, check for uniqueness
            if profile_update.user_id and profile_update.user_id != profile.user_id:
                existing_profile = await self.onboarding_profile_repository.get_onboarding_profile_by_user_id(profile_update.user_id)
                if existing_profile:
                    logger.warning(f"Attempted to update onboarding profile with duplicate user_id: {profile_update.user_id}")
                    raise HTTPException(
                        status_code=409,
                        detail="Another onboarding profile with this user_id already exists."
                    )

            # Validate Master Love To IDs if provided
            if profile_update.master_love_to_ids is not None:
                valid_love_to_ids = await self.master_love_to_repository.get_valid_ids(profile_update.master_love_to_ids)
                invalid_love_to_ids = set(profile_update.master_love_to_ids) - set(valid_love_to_ids)
                if invalid_love_to_ids:
                    logger.warning(f"Invalid Master Love To IDs: {sorted(invalid_love_to_ids)}")
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid Master Love To IDs: {sorted(invalid_love_to_ids)}"
                    )

            # Validate Master Previous Dive Site IDs if provided
            if profile_update.master_previous_dive_site_ids is not None:
                valid_previous_site_ids = await self.master_previous_dive_site_repository.get_valid_ids(profile_update.master_previous_dive_site_ids)
                invalid_previous_site_ids = set(profile_update.master_previous_dive_site_ids) - set(valid_previous_site_ids)
                if invalid_previous_site_ids:
                    logger.warning(f"Invalid Master Previous Dive Site IDs: {sorted(invalid_previous_site_ids)}")
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid Master Previous Dive Site IDs: {sorted(invalid_previous_site_ids)}"
                    )

            # Update profile fields
            updated_profile = await self.onboarding_profile_repository.update_onboarding_profile(profile_id, profile_update)
            if not updated_profile:
                logger.error(f"Failed to update onboarding profile with ID: {profile_id}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to update the onboarding profile."
                )

            # Synchronize profile_love_tos if provided
            if profile_update.master_love_to_ids is not None:
                await self.onboarding_profile_repository.synchronize_profile_love_tos(
                    profile=updated_profile,
                    master_love_to_ids=profile_update.master_love_to_ids
                )

            # Synchronize profile_previous_dive_sites if provided
            if profile_update.master_previous_dive_site_ids is not None:
                await self.onboarding_profile_repository.synchronize_profile_previous_dive_sites(
                    profile=updated_profile,
                    master_previous_dive_site_ids=profile_update.master_previous_dive_site_ids
                )

            # Commit the changes
            await self.onboarding_profile_repository.db.commit()
            await self.onboarding_profile_repository.db.refresh(updated_profile)

            # Fetch the updated profile with relations
            created_profile = await self.onboarding_profile_repository.get_onboarding_profile_by_id(updated_profile.id)
            if not created_profile:
                logger.error(f"Failed to retrieve the updated onboarding profile with ID: {updated_profile.id}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to retrieve the updated onboarding profile."
                )
            logger.info(f"Updated onboarding profile with ID: {created_profile.id}")
            return OnboardingProfileWithRelations.from_orm(created_profile)
        except IntegrityError as e:
            logger.exception("IntegrityError occurred while updating onboarding profile with associations.")
            raise HTTPException(status_code=400, detail="Integrity error occurred.")
        except HTTPException as he:
            logger.error(f"HTTPException occurred: {he.detail}")
            raise he
        except Exception as e:
            logger.exception("Unexpected error occurred while updating onboarding profile with associations.")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def delete_onboarding_profile(self, profile_id: int) -> bool:
        return await self.onboarding_profile_repository.delete_onboarding_profile(profile_id)