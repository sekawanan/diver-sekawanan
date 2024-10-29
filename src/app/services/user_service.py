# app/services/users_service.py
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all_users(self) -> List[User]:
        return await self.repository.get_all_users()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        return await self.repository.get_user_by_id(user_id)

    async def create_user(self, user_create: UserCreate) -> User:
        try:
            return await self.repository.create_user(user_create)
        except IntegrityError as e:
            # Log the error as needed
            raise ValueError("Username or email already exists.") from e

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        try:
            return await self.repository.update_user(user_id, user_update)
        except IntegrityError as e:
            # Log the error as needed
            raise ValueError("Username or email already exists.") from e

    async def delete_user(self, user_id: int) -> bool:
        return await self.repository.delete_user(user_id)