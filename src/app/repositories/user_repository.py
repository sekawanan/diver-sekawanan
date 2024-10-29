from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate  # Assuming you have a UserUpdate schema


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_user(self, user_create: UserCreate) -> User:
        user = User(
            username=user_create.username,
            fullname=user_create.fullname,
            email=user_create.email,
            is_active=user_create.is_active,
            # Assume password hashing is handled elsewhere
        )
        self.db.add(user)
        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError:
            await self.db.rollback()
            raise

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(user, field, value)
        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError:
            await self.db.rollback()
            raise

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True