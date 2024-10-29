import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.schemas.diver import DiverWithLicenses
from app.database.session import get_db
from app.models.diver_profile import DiverProfile
from app.models.dive_preference import DivePreference
from app.models.diver_license import DiverLicense

# Initialize logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

api_router = APIRouter()

@api_router.get("/diver-license", response_model=DiverWithLicenses)
async def read_license(
    diver_profile_id: int,
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Fetching diver_profile_id={diver_profile_id}")

    query = select(DiverProfile).options(
        selectinload(DiverProfile.licenses).selectinload(DiverLicense.master_license),
        selectinload(DiverProfile.dive_preferences).selectinload(DivePreference.master_preference)
    ).where(DiverProfile.id == diver_profile_id)

    result = await db.execute(query)
    diver = result.scalars().first()

    if not diver:
        logger.warning(f"Diver with profile ID {diver_profile_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diver not found")

    # Prepare licenses list
    licenses_list = [
        {
            "id": license.id,
            "master_license_id": license.master_license_id,
            "certification_number": license.certification_number,
            "created_at": license.created_at.isoformat() if license.created_at else None,  # Handle None
            "modified_at": license.modified_at.isoformat() if license.modified_at else None  # Handle None
        }
        for license in diver.licenses
    ]

    # Prepare dive preferences list with labels
    dive_prefs_list = [
        {
            "id": pref.id,
            "diver_profile_id": pref.diver_profile_id,
            "master_dive_preference_id": pref.master_dive_preference_id,
            "label": pref.master_preference.label if pref.master_preference else None
        }
        for pref in diver.dive_preferences
    ]

    # Handle diver's datetime fields
    diver_created_at = diver.created_at.isoformat() if diver.created_at else None
    diver_modified_at = diver.modified_at.isoformat() if diver.modified_at else None

    logger.info(f"Diver profile ID {diver_profile_id} fetched successfully.")

    return JSONResponse(
        content={
            "status": "success",
            "message": "Diver info fetched successfully",
            "data": {
                "diver_profile_id": diver.id,
                "user_id": diver.user_id,
                "first_name": diver.first_name,
                "last_name": diver.last_name,
                "created_at": diver_created_at,
                "modified_at": diver_modified_at,
                "licenses": licenses_list,
                "dive_preferences": dive_prefs_list
            }
        },
        status_code=200
    )
