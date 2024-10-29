# app/services/favorite_marine_life_service.py

from typing import List, Optional
from app.repositories.favorite_marine_life_repository import FavoriteMarineLifeRepository
from app.schemas.favorite_marine_life import (
    FavoriteMarineLifeCreate,
    FavoriteMarineLifeCreateMultiple,
    FavoriteMarineLifeUpdate,
    FavoriteMarineLifeRead,
)
from app.models.favorite_marine_life import FavoriteMarineLife
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

import logging

logger = logging.getLogger(__name__)

class DuplicateFavoriteMarineLifeError(Exception):
    """Custom exception for duplicate favorite marine life entries."""
    def __init__(self, diver_profile_id: int, master_marine_life_id: int):
        self.diver_profile_id = diver_profile_id
        self.master_marine_life_id = master_marine_life_id
        self.message = f"Diver with profile_id {diver_profile_id} already has master_marine_life_id {master_marine_life_id}."
        super().__init__(self.message)

class FavoriteMarineLifeService:
    def __init__(self, repository: FavoriteMarineLifeRepository):
        self.repository = repository

    async def get_favorites_by_diver(self, diver_profile_id: int) -> List[FavoriteMarineLife]:
        try:
            favorites = await self.repository.get_favorites_by_diver(diver_profile_id)
            # Return empty list if no records found
            if not favorites:
                return []
            
            for favorite in favorites:
                if not favorite.master_marine_life:
                    raise ValueError(f"MasterMarineLife entry missing for favorite marine life ID {favorite.id}")

            return favorites
        
        except Exception as e:
            logger.error(f"Error retrieving favorites: {e}")
            raise e

    async def create_favorite(self, diver_profile_id: int, favorite_data: FavoriteMarineLifeCreate) -> FavoriteMarineLife:
        try:
            # Check for duplicates
            existing_favorite = await self.repository.get_favorite_by_master_id(diver_profile_id, favorite_data.master_marine_life_id)
            if existing_favorite:
                logger.warning(f"Duplicate favorite marine life detected for diver_profile_id {diver_profile_id} and master_marine_life_id {favorite_data.master_marine_life_id}.")
                raise DuplicateFavoriteMarineLifeError(diver_profile_id, favorite_data.master_marine_life_id)
            
            new_favorite = await self.repository.create_favorite(diver_profile_id, favorite_data)
            if not new_favorite:
                logger.error("Failed to create favorite marine life due to IntegrityError.")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid master_marine_life_id provided."
                )
            return new_favorite
        except DuplicateFavoriteMarineLifeError as e:
            logger.error(e.message)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=e.message
            ) from e
        except IntegrityError as e:
            logger.error(f"IntegrityError during creation: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid master_marine_life_id provided."
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error during creation: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the favorite marine life."
            ) from e

    async def create_favorites_bulk(self, diver_profile_id: int, favorite_data: FavoriteMarineLifeCreateMultiple) -> List[FavoriteMarineLife]:
        try:
            # Fetch existing favorites to avoid duplicates
            existing_favorites = await self.repository.get_favorites_by_diver(diver_profile_id)
            existing_master_ids = {fav.master_marine_life_id for fav in existing_favorites}
            logger.info(f"Existing master_marine_life_ids for diver_profile_id {diver_profile_id}: {existing_master_ids}")
            
            # Filter out duplicates
            unique_master_ids = [mid for mid in favorite_data.master_marine_life_ids if mid not in existing_master_ids]
            logger.info(f"Unique master_marine_life_ids to create: {unique_master_ids}")
            
            if not unique_master_ids:
                logger.warning(f"No new favorite marine life entries to create for diver_profile_id {diver_profile_id}. All preferences already exist.")
                return []  # Empty list
            
            # Create in bulk
            new_favorites = await self.repository.create_favorites_bulk(diver_profile_id, unique_master_ids)
            return new_favorites
        except IntegrityError as e:
            logger.error(f"IntegrityError during bulk creation: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more master_marine_life_ids are invalid."
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error during bulk creation: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating favorite marine life entries."
            ) from e

    async def update_favorite(self, diver_profile_id: int, favorite_id: int, favorite_update: FavoriteMarineLifeUpdate) -> FavoriteMarineLife:
        try:
            # If updating the master_marine_life_id, ensure it's not creating a duplicate
            if favorite_update.master_marine_life_id is not None:
                existing_favorite = await self.repository.get_favorite_by_master_id(diver_profile_id, favorite_update.master_marine_life_id)
                if existing_favorite and existing_favorite.id != favorite_id:
                    logger.warning(f"Duplicate favorite marine life detected for diver_profile_id {diver_profile_id} and master_marine_life_id {favorite_update.master_marine_life_id}.")
                    raise DuplicateFavoriteMarineLifeError(diver_profile_id, favorite_update.master_marine_life_id)
            
            updated_favorite = await self.repository.update_favorite(diver_profile_id, favorite_id, favorite_update)
            if not updated_favorite:
                logger.warning(f"FavoriteMarineLife with id {favorite_id} not found for diver_profile_id {diver_profile_id}.")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Favorite marine life with id {favorite_id} not found for diver_profile_id {diver_profile_id}."
                )
            return updated_favorite
        except DuplicateFavoriteMarineLifeError as e:
            logger.error(e.message)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=e.message
            ) from e
        except IntegrityError as e:
            logger.error(f"IntegrityError during update: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid master_marine_life_id provided."
            ) from e
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Unexpected error during update: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the favorite marine life."
            ) from e

    async def delete_favorite(self, diver_profile_id: int, favorite_id: int) -> bool:
        try:
            success = await self.repository.delete_favorite(diver_profile_id, favorite_id)
            if not success:
                logger.warning(f"FavoriteMarineLife with id {favorite_id} not found for diver_profile_id {diver_profile_id}.")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Favorite marine life with id {favorite_id} not found for diver_profile_id {diver_profile_id}."
                )
            return success
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Unexpected error during deletion: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the favorite marine life."
            ) from e