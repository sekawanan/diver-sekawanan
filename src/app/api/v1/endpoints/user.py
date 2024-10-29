# app/api/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
# from app.api.dependencies import get_current_user
from typing import List
from app.schemas.base_response import BaseResponse
from app.schemas.user import TokenInput, UserCreate, UserRead, UserWithProfiles, UserUpdate
from app.services.user_service import UserService
from app.core.jwt_manager import JWTManager
# from app.use_cases.token_use_cases import revoke_all_user_tokens
from app.core.config import settings
from app.dependencies import get_user_service
jwt_manager = JWTManager(secret_key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

api_router = APIRouter()

# Endpoint to decode token
@api_router.post("/decode-token")
def decode_token(input: TokenInput):
    """
    Decodes a JWT token and returns its payload.
    """
    try:
        payload = jwt_manager.decode_token(input.token)
        return {"payload": payload}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred: {str(e)}"
        )

@api_router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Adds a new user to the system.",
)
async def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """
    Create a new user.
    """
    try:
        created_user = await service.create_user(user)
        logger.info(f"Created user with ID: {created_user.id}")
        return created_user
    except ValueError as ve:
        logger.error(f"Error creating user: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )

@api_router.get(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a user by ID",
    description="Fetches a user by their unique ID.",
)
async def read_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """
    Retrieve a user by ID.
    """
    user = await service.get_user_by_id(user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    logger.info(f"Retrieved user with ID: {user_id}")
    return user

@api_router.get(
    "/",
    response_model=List[UserRead],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all users",
    description="Fetches a list of all users.",
)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service)
):
    """
    Retrieve all users with pagination.
    """
    users = await service.get_all_users(skip=skip, limit=limit)
    logger.info(f"Retrieved {len(users)} users.")
    return users

@api_router.put(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    description="Updates the details of an existing user.",
)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    """
    Update an existing user.
    """
    updated_user = await service.update_user(user_id, user_update)
    if not updated_user:
        logger.warning(f"User with ID {user_id} not found for update.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    logger.info(f"Updated user with ID: {user_id}")
    return updated_user

@api_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Removes a user from the system.",
)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """
    Delete a user.
    """
    success = await service.delete_user(user_id)
    if not success:
        logger.warning(f"User with ID {user_id} not found for deletion.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    logger.info(f"Deleted user with ID: {user_id}")
    return