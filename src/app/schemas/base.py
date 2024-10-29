# app/schemas/base.py

from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    status: str
    data: Optional[T] = None
    message: Optional[str] = None