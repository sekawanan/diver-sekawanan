# app/api/v1/endpoints/favorite_marine_life.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.favorite_marine_life import (
    FavoriteMarineLifeRead,
    FavoriteMarineLifeCreate,
    FavoriteMarineLifeCreateMultiple,
    FavoriteMarineLifeUpdate,
)
from app.services.favorite_marine_life_service import FavoriteMarineLifeService
from app.dependencies import get_favorite_marine_life_service

import logging

logger = logging.getLogger(__name__)

api_router = APIRouter()

@api_router.get(
    "/{diver_profile_id}",
    response_model=List[FavoriteMarineLifeRead],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all favorite marine life for a diver",
    tags=["Favorite Marine Life"]
)
async def read_favorite_marine_life(
    diver_profile_id: int,
    service: FavoriteMarineLifeService = Depends(get_favorite_marine_life_service)
):
    """
    Retrieve all favorite marine life associated with a specific diver profile ID.
    """
    try:
        favorites = await service.get_favorites_by_diver(diver_profile_id)
        if not favorites:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No favorite marine life found for diver_profile_id {diver_profile_id}.",
            )
        return favorites
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving favorite marine life entries.",
        ) from e
    
@api_router.post(
    "/{diver_profile_id}/batch",
    response_model=List[FavoriteMarineLifeRead],
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple favorite marine life entries for a diver",
    tags=["Favorite Marine Life"]
)
async def create_multiple_favorite_marine_life(
    diver_profile_id: int,
    favorite_data: FavoriteMarineLifeCreateMultiple,
    service: FavoriteMarineLifeService = Depends(get_favorite_marine_life_service)
):
    """
    Create multiple favorite marine life entries for a specific diver profile.
    """
    try:
        new_favorites = await service.create_favorites_bulk(diver_profile_id, favorite_data)
        if not new_favorites:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No new favorite marine life entries were created. They may already exist."
            )
        return new_favorites
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error creating favorite marine life entries: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating favorite marine life entries."
        ) from e

@api_router.post(
    "/{diver_profile_id}",
    response_model=FavoriteMarineLifeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new favorite marine life entry for a diver",
    tags=["Favorite Marine Life"]
)
async def create_favorite_marine_life(
    diver_profile_id: int,
    favorite_data: FavoriteMarineLifeCreate,
    service: FavoriteMarineLifeService = Depends(get_favorite_marine_life_service)
):
    """
    Create a new favorite marine life entry for a specific diver profile.
    """
    try:
        new_favorite = await service.create_favorite(diver_profile_id, favorite_data)
        return new_favorite
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error creating favorite marine life entry: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the favorite marine life entry."
        ) from e

@api_router.put(
    "/{diver_profile_id}/{favorite_id}",
    response_model=FavoriteMarineLifeRead,
    status_code=status.HTTP_200_OK,
    summary="Update an existing favorite marine life entry for a diver",
    tags=["Favorite Marine Life"]
)
async def update_favorite_marine_life(
    diver_profile_id: int,
    favorite_id: int,
    favorite_update: FavoriteMarineLifeUpdate,
    service: FavoriteMarineLifeService = Depends(get_favorite_marine_life_service)
):
    """
    Update an existing favorite marine life entry for a specific diver profile.
    """
    try:
        updated_favorite = await service.update_favorite(diver_profile_id, favorite_id, favorite_update)
        return updated_favorite
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating favorite marine life entry: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the favorite marine life entry."
        ) from e

@api_router.delete(
    "/{diver_profile_id}/{favorite_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Delete a favorite marine life entry for a diver",
    tags=["Favorite Marine Life"]
)
async def delete_favorite_marine_life(
    diver_profile_id: int,
    favorite_id: int,
    service: FavoriteMarineLifeService = Depends(get_favorite_marine_life_service)
):
    """
    Delete an existing favorite marine life entry for a specific diver profile.
    """
    try:
        success = await service.delete_favorite(diver_profile_id, favorite_id)
        return {"detail": f"Favorite marine life entry with id {favorite_id} deleted successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting favorite marine life entry: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the favorite marine life entry."
        ) from e