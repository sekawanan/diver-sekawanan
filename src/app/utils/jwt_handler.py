import jwt
from typing import Optional, Dict, Any
from app.core.config import settings
from jose import JWTError, jwt 
from datetime import datetime, timedelta
from pydantic import BaseModel, ValidationError

class TokenPayload(BaseModel):
    user_id: str
    exp: datetime
    iat: datetime
    nbf: datetime
    iss: str
    aud: str
    type: str

class JWTHandler:
    @staticmethod
    def decode_token(token: str, token_type: str) -> Optional[TokenPayload]:
        """
        Decode and validate a JWT token.

        Args:
            token (str): The JWT token string.
            token_type (str): Expected token type ('access' or 'refresh').

        Returns:
            Optional[TokenPayload]: Parsed token payload if valid, else None.
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
                issuer=settings.ISSUER,
                audience=settings.AUDIENCE,
            )
            # Validate the 'type' claim
            if payload.get("type") != token_type:
                return None
            # Parse and validate payload using Pydantic
            token_data = TokenPayload(**payload)
            return token_data
        except (JWTError, ValidationError) as e:
            print(e)
            return None

    @staticmethod
    def decode_access_token(token: str) -> Optional[TokenPayload]:
        """
        Decode and validate an access token.

        Args:
            token (str): The JWT access token string.

        Returns:
            Optional[TokenPayload]: Parsed token payload if valid, else None.
        """
        return JWTHandler.decode_token(token, "access")