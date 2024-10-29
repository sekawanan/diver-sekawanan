# app/repositories/favorite_marine_life_repository.py

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.models.favorite_marine_life import FavoriteMarineLife
from app.schemas.favorite_marine_life import (
    FavoriteMarineLifeCreate,
    FavoriteMarineLifeUpdate,
)
from app.models.master_marine_life import MasterMarineLife
from app.models.diver_profile import DiverProfile

import logging

# Configure logger
logger = logging.getLogger(__name__)

class FavoriteMarineLifeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_favorites_by_diver(self, diver_profile_id: int) -> List[FavoriteMarineLife]:
        result = await self.db.execute(
            select(FavoriteMarineLife)
            .options(selectinload(FavoriteMarineLife.master_marine_life))
            .where(FavoriteMarineLife.diver_profile_id == diver_profile_id)
        )
        favorites = result.scalars().all()
        logger.info(f"Retrieved {len(favorites)} favorite marine life entries for diver_profile_id {diver_profile_id}.")
        return favorites

    async def get_favorite_by_id(self, diver_profile_id: int, favorite_id: int) -> Optional[FavoriteMarineLife]:
        result = await self.db.execute(
            select(FavoriteMarineLife)
            .options(selectinload(FavoriteMarineLife.master_marine_life))
            .where(
                FavoriteMarineLife.diver_profile_id == diver_profile_id,
                FavoriteMarineLife.id == favorite_id
            )
        )
        favorite = result.scalar_one_or_none()
        return favorite

    async def get_favorite_by_master_id(self, diver_profile_id: int, master_marine_life_id: int) -> Optional[FavoriteMarineLife]:
        result = await self.db.execute(
            select(FavoriteMarineLife)
            .where(
                FavoriteMarineLife.diver_profile_id == diver_profile_id,
                FavoriteMarineLife.master_marine_life_id == master_marine_life_id
            )
        )
        favorite = result.scalar_one_or_none()
        return favorite

    async def create_favorite(self, diver_profile_id: int, favorite_data: FavoriteMarineLifeCreate) -> Optional[FavoriteMarineLife]:
        new_favorite = FavoriteMarineLife(
            diver_profile_id=diver_profile_id,
            master_marine_life_id=favorite_data.master_marine_life_id
        )
        self.db.add(new_favorite)
        try:
            await self.db.commit()
            await self.db.refresh(new_favorite)
            # Eagerly load the master_marine_life
            result = await self.db.execute(
                select(FavoriteMarineLife)
                .options(selectinload(FavoriteMarineLife.master_marine_life))
                .where(FavoriteMarineLife.id == new_favorite.id)
            )
            new_favorite = result.scalar_one()
            logger.info(f"Created FavoriteMarineLife with id {new_favorite.id} for diver_profile_id {diver_profile_id}.")
            return new_favorite
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"IntegrityError: {e}")
            return None  # Handle in service layer

    async def create_favorites_bulk(self, diver_profile_id: int, master_marine_life_ids: List[int]) -> List[FavoriteMarineLife]:
        new_favorites = [
            FavoriteMarineLife(
                diver_profile_id=diver_profile_id,
                master_marine_life_id=mid
            )
            for mid in master_marine_life_ids
        ]
        self.db.add_all(new_favorites)
        logger.info(f"Attempting to create {len(new_favorites)} favorite marine life entries for diver_profile_id {diver_profile_id}.")
        try:
            await self.db.commit()
            for fav in new_favorites:
                await self.db.refresh(fav)
                logger.info(f"Successfully created FavoriteMarineLife with id {fav.id}, master_marine_life_id {fav.master_marine_life_id}.")
            # Eagerly load master_marine_life
            result = await self.db.execute(
                select(FavoriteMarineLife)
                .options(selectinload(FavoriteMarineLife.master_marine_life))
                .where(
                    FavoriteMarineLife.diver_profile_id == diver_profile_id,
                    FavoriteMarineLife.master_marine_life_id.in_(master_marine_life_ids)
                )
            )
            created_favorites = result.scalars().all()
            return created_favorites
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"IntegrityError during bulk creation: {e}")
            raise e  # Let service layer handle
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Unexpected error during bulk creation: {e}")
            raise e

    async def update_favorite(self, diver_profile_id: int, favorite_id: int, favorite_update: FavoriteMarineLifeUpdate) -> Optional[FavoriteMarineLife]:
        favorite = await self.get_favorite_by_id(diver_profile_id, favorite_id)
        if not favorite:
            logger.warning(f"FavoriteMarineLife with id {favorite_id} not found for diver_profile_id {diver_profile_id}.")
            return None

        update_data = favorite_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(favorite, key, value)

        self.db.add(favorite)
        try:
            await self.db.commit()
            await self.db.refresh(favorite)
            # Eagerly load the master_marine_life
            result = await self.db.execute(
                select(FavoriteMarineLife)
                .options(selectinload(FavoriteMarineLife.master_marine_life))
                .where(FavoriteMarineLife.id == favorite.id)
            )
            updated_favorite = result.scalar_one()
            logger.info(f"Updated FavoriteMarineLife with id {favorite.id} for diver_profile_id {diver_profile_id}.")
            return updated_favorite
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"IntegrityError during update: {e}")
            return None  # Handle in service layer

    async def delete_favorite(self, diver_profile_id: int, favorite_id: int) -> bool:
        favorite = await self.get_favorite_by_id(diver_profile_id, favorite_id)
        if not favorite:
            logger.warning(f"FavoriteMarineLife with id {favorite_id} not found for diver_profile_id {diver_profile_id}.")
            return False
        await self.db.delete(favorite)
        try:
            await self.db.commit()
            logger.info(f"Deleted FavoriteMarineLife with id {favorite_id} for diver_profile_id {diver_profile_id}.")
            return True
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"IntegrityError during deletion: {e}")
            return False
