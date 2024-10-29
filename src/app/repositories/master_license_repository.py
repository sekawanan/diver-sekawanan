# app/repositories/master_license_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.master_license import MasterLicense

class MasterLicenseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_master_license_by_id(self, master_license_id: int) -> Optional[MasterLicense]:
        result = await self.db.execute(select(MasterLicense).where(MasterLicense.id == master_license_id))
        return result.scalars().first()

    async def get_all_master_licenses(self) -> List[MasterLicense]:
        result = await self.db.execute(select(MasterLicense))
        licenses = result.scalars().all()
        return licenses

    async def create_master_license(self, master_license: MasterLicense) -> MasterLicense:
        self.db.add(master_license)
        await self.db.commit()
        await self.db.refresh(master_license)
        return master_license

    async def update_master_license(self, master_license_id: int, master_license_data: dict) -> Optional[MasterLicense]:
        result = await self.db.execute(select(MasterLicense).where(MasterLicense.id == master_license_id))
        master_license = result.scalars().first()
        if master_license:
            for key, value in master_license_data.items():
                setattr(master_license, key, value)
            await self.db.commit()
            await self.db.refresh(master_license)
        return master_license

    async def delete_master_license(self, master_license_id: int) -> bool:
        result = await self.db.execute(select(MasterLicense).where(MasterLicense.id == master_license_id))
        master_license = result.scalars().first()
        if master_license:
            await self.db.delete(master_license)
            await self.db.commit()
            return True
        return False