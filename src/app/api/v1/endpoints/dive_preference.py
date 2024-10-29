# app/api/v1/endpoints/dive_preference.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError  # Added IntegrityError import
from app.schemas.dive_preference import (
    DivePreferenceRead,
    DivePreferenceCreate,
    DivePreferenceCreateMultiple,
    DivePreferenceUpdate,
)
from app.services.dive_preference_service import DivePreferenceService, DuplicateDivePreferenceError
from app.dependencies import get_dive_preference_service

api_router = APIRouter()

@api_router.get(
    "/dive-preferences/{diver_profile_id}",
    response_model=List[DivePreferenceRead],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all dive preferences for a diver",
)
async def read_diver_preferences(
    diver_profile_id: int,
    service: DivePreferenceService = Depends(get_dive_preference_service)
):
    """
    Retrieve all dive preferences associated with a specific diver profile ID.
    """
    try:
        preferences = await service.get_preferences_by_diver(diver_profile_id)
        if not preferences:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No dive preferences found for diver_profile_id {diver_profile_id}.",
            )
        return preferences
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving dive preferences."
        ) from e

@api_router.post(
    "/dive-preferences/{diver_profile_id}/batch",
    response_model=List[DivePreferenceRead],  # List of created preferences
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple dive preferences for a diver",
)
async def create_multiple_diver_preferences(
    diver_profile_id: int,
    preference_data: DivePreferenceCreateMultiple,
    service: DivePreferenceService = Depends(get_dive_preference_service)
):
    """
    Create multiple dive preferences for a specific diver profile.
    """
    try:
        new_preferences = await service.create_preferences_bulk(diver_profile_id, preference_data)
        if not new_preferences:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No new dive preferences were created. They may already exist."
            )
        return new_preferences
    except DuplicateDivePreferenceError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        ) from e
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more master_dive_preference_ids are invalid."
        ) from e
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the dive preferences."
        ) from e

@api_router.post(
    "/dive-preferences/{diver_profile_id}",
    response_model=DivePreferenceRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new dive preference for a diver",
)
async def create_diver_preference(
    diver_profile_id: int,
    preference_data: DivePreferenceCreate,
    service: DivePreferenceService = Depends(get_dive_preference_service)
):
    """
    Create a new dive preference for a specific diver profile.
    """
    try:
        new_preference = await service.create_preference(diver_profile_id, preference_data)
        return new_preference
    except DuplicateDivePreferenceError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        ) from e
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid master_dive_preference_id."
        ) from e
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the dive preference."
        ) from e

@api_router.put(
    "/dive-preferences/{diver_profile_id}/{preference_id}",
    response_model=DivePreferenceRead,
    status_code=status.HTTP_200_OK,
    summary="Update an existing dive preference for a diver",
)
async def update_diver_preference(
    diver_profile_id: int,
    preference_id: int,
    preference_update: DivePreferenceUpdate,
    service: DivePreferenceService = Depends(get_dive_preference_service)
):
    """
    Update an existing dive preference for a specific diver profile.
    """
    try:
        updated_preference = await service.update_preference(diver_profile_id, preference_id, preference_update)
        if not updated_preference:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dive preference with id {preference_id} not found for diver_profile_id {diver_profile_id}.",
            )
        return updated_preference
    except DuplicateDivePreferenceError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        ) from e
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid master_dive_preference_id."
        ) from e
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the dive preference."
        ) from e

@api_router.delete(
    "/dive-preferences/{diver_profile_id}/{preference_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Delete a dive preference for a diver",
)
async def delete_diver_preference(
    diver_profile_id: int,
    preference_id: int,
    service: DivePreferenceService = Depends(get_dive_preference_service)
):
    """
    Delete an existing dive preference for a specific diver profile.
    """
    try:
        success = await service.delete_preference(diver_profile_id, preference_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dive preference with id {preference_id} not found for diver_profile_id {diver_profile_id}.",
            )
        return {"detail": f"Dive preference with id {preference_id} deleted successfully."}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the dive preference."
        ) from e