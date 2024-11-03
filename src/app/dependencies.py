# app/dependencies.py

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
import logging

from app.database.session import async_session
from app.repositories.diver_license_repository import DiverLicenseRepository
from app.repositories.diver_profile_repository import DiverProfileRepository
from app.repositories.master_license_repository import MasterLicenseRepository
from app.repositories.dive_preference_repository import DivePreferenceRepository
from app.repositories.favorite_marine_life_repository import FavoriteMarineLifeRepository
from app.repositories.master_gear_repository import MasterGearRepository
from app.repositories.master_color_repository import MasterColorRepository

from app.repositories.onboarding_profile_repository import OnboardingProfileRepository
from app.repositories.master_love_to_repository import MasterLoveToRepository
from app.repositories.master_previous_dive_site_repository import MasterPreviousDiveSiteRepository
from app.repositories.profile_love_to_repository import ProfileLoveToRepository
from app.repositories.profile_previous_dive_site_repository import ProfilePreviousDiveSiteRepository

from app.services.diver_license_service import DiverLicenseService
from app.services.diver_profile_service import DiverProfileService
from app.services.master_license_service import MasterLicenseService
from app.services.dive_preference_service import DivePreferenceService
from app.services.favorite_marine_life_service import FavoriteMarineLifeService
from app.services.master_gear_service import MasterGearService
from app.services.master_color_service import MasterColorService

from app.services.onboarding_profile_service import OnboardingProfileService
from app.services.master_love_to_service import MasterLoveToService
from app.services.master_previous_dive_site_service import MasterPreviousDiveSiteService
from app.services.profile_love_to_service import ProfileLoveToService
from app.services.profile_previous_dive_site_service import ProfilePreviousDiveSiteService
from app.database.session import get_db
from app.core.jwt_manager import JWTManager
from app.core.config import settings

logger = logging.getLogger(__name__)

# Database Dependency
# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session() as session:
#         try:
#             yield session
#         except Exception as e:
#             logger.error(f"Database session error: {e}")
#             raise e

# JWT Manager Dependency
def get_jwt_manager() -> JWTManager:
    return JWTManager(secret_key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Repository Dependencies

def get_diver_license_repository(db: AsyncSession = Depends(get_db)) -> DiverLicenseRepository:
    return DiverLicenseRepository(db)

def get_diver_profile_repository(db: AsyncSession = Depends(get_db)) -> DiverProfileRepository:
    return DiverProfileRepository(db)

def get_master_license_repository(db: AsyncSession = Depends(get_db)) -> MasterLicenseRepository:
    return MasterLicenseRepository(db)

def get_dive_preference_repository(db: AsyncSession = Depends(get_db)) -> DivePreferenceRepository:
    return DivePreferenceRepository(db)

def get_favorite_marine_life_repository(db: AsyncSession = Depends(get_db)) -> FavoriteMarineLifeRepository:
    return FavoriteMarineLifeRepository(db)

def get_master_gear_repository(db: AsyncSession = Depends(get_db)) -> MasterGearRepository:
    return MasterGearRepository(db)

def get_master_color_repository(db: AsyncSession = Depends(get_db)) -> MasterColorRepository:
    return MasterColorRepository(db)

def get_onboarding_profile_repository(db: AsyncSession = Depends(get_db)) -> OnboardingProfileRepository:
    return OnboardingProfileRepository(db)

def get_master_love_to_repository(db: AsyncSession = Depends(get_db)) -> MasterLoveToRepository:
    return MasterLoveToRepository(db)

def get_master_previous_dive_site_repository(db: AsyncSession = Depends(get_db)) -> MasterPreviousDiveSiteRepository:
    return MasterPreviousDiveSiteRepository(db)

def get_profile_love_to_repository(db: AsyncSession = Depends(get_db)) -> ProfileLoveToRepository:
    return ProfileLoveToRepository(db)

def get_profile_previous_dive_site_repository(db: AsyncSession = Depends(get_db)) -> ProfilePreviousDiveSiteRepository:
    return ProfilePreviousDiveSiteRepository(db)

# Service Dependencies

def get_diver_license_service(
    license_repo: DiverLicenseRepository = Depends(get_diver_license_repository),
    profile_repo: DiverProfileRepository = Depends(get_diver_profile_repository),
    master_license_repo: MasterLicenseRepository = Depends(get_master_license_repository)
) -> DiverLicenseService:
    return DiverLicenseService(
        license_repository=license_repo,
        profile_repository=profile_repo,
        master_license_repository=master_license_repo
    )

def get_diver_profile_service(
    repository: DiverProfileRepository = Depends(get_diver_profile_repository)
) -> DiverProfileService:
    return DiverProfileService(repository)

def get_master_license_service(
    master_license_repo: MasterLicenseRepository = Depends(get_master_license_repository)
) -> MasterLicenseService:
    return MasterLicenseService(master_license_repository=master_license_repo)

def get_dive_preference_service(
    repository: DivePreferenceRepository = Depends(get_dive_preference_repository)
) -> DivePreferenceService:
    return DivePreferenceService(repository)

def get_favorite_marine_life_service(
    repository: FavoriteMarineLifeRepository = Depends(get_favorite_marine_life_repository)
) -> FavoriteMarineLifeService:
    return FavoriteMarineLifeService(repository)

def get_master_gear_service(
    repository: MasterGearRepository = Depends(get_master_gear_repository)
) -> MasterGearService:
    return MasterGearService(repository)

def get_master_color_service(
    repository: MasterColorRepository = Depends(get_master_color_repository)
) -> MasterColorService:
    return MasterColorService(repository)
# def get_onboarding_profile_service(
#     onboarding_repo: OnboardingProfileRepository = Depends(get_onboarding_profile_repository)
# ) -> OnboardingProfileService:
#     return OnboardingProfileService(repository=onboarding_repo)

def get_onboarding_profile_service(
    onboarding_profile_repo: OnboardingProfileRepository = Depends(get_onboarding_profile_repository),
    master_love_to_repo: MasterLoveToRepository = Depends(get_master_love_to_repository),
    master_previous_dive_site_repo: MasterPreviousDiveSiteRepository = Depends(get_master_previous_dive_site_repository)
) -> OnboardingProfileService:
    return OnboardingProfileService(
        onboarding_profile_repository=onboarding_profile_repo,
        master_love_to_repository=master_love_to_repo,
        master_previous_dive_site_repository=master_previous_dive_site_repo
    )

def get_master_love_to_service(
    master_love_to_repo: MasterLoveToRepository = Depends(get_master_love_to_repository)
) -> MasterLoveToService:
    return MasterLoveToService(master_love_to_repository=master_love_to_repo)

def get_master_previous_dive_site_service(
    master_previous_dive_site_repo: MasterPreviousDiveSiteRepository = Depends(get_master_previous_dive_site_repository)
) -> MasterPreviousDiveSiteService:
    return MasterPreviousDiveSiteService(master_previous_dive_site_repository=master_previous_dive_site_repo)

def get_profile_love_to_service(
    profile_love_to_repo: ProfileLoveToRepository = Depends(get_profile_love_to_repository)
) -> ProfileLoveToService:
    return ProfileLoveToService(profile_love_to_repository=profile_love_to_repo)

def get_profile_previous_dive_site_service(
    profile_previous_dive_site_repo: ProfilePreviousDiveSiteRepository = Depends(get_profile_previous_dive_site_repository)
) -> ProfilePreviousDiveSiteService:
    return ProfilePreviousDiveSiteService(profile_previous_dive_site_repository=profile_previous_dive_site_repo)