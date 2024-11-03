# app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.jwt_manager import JWTManager
from fastapi import Depends, HTTPException, Header, status
from typing import Optional
from app.utils.jwt_handler import JWTHandler, TokenPayload
from app.core.config import settings

async def get_current_user_id(authorization: str) -> str:
    """
    Dependency to extract and validate the current user's username from the access token.

    Args:
        authorization (Optional[str]): The Authorization header.

    Returns:
        str: The username extracted from the token.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme or token missing.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_payload: Optional[TokenPayload] = JWTHandler.decode_access_token(token)
    if token_payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(token_payload)
    
    user_id: Optional[str] = token_payload.user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user_id not found in token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print("-----------")
    print(user_id)
    print("-----------")
    
    return user_id