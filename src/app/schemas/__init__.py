# app/schemas/__init__.py

# 1. Import Master Schemas First
from .master_license import MasterLicenseRead
from .master_dive_preference import MasterDivePreferenceRead
from .master_dive_site import MasterDiveSiteRead
from .master_gear import MasterGearRead
from .master_brand import MasterBrandRead
from .master_gear_brand import MasterGearBrandRead
from .master_color import MasterColorRead
from .master_marine_life import MasterMarineLifeRead
from .master_dive_type import MasterDiveTypeRead

# 2. Import Dependent Schemas Next
from .diver_license import DiverLicenseCreate, DiverLicenseRead, DiverLicenseUpdate
from .dive_preference import DivePreferenceCreate, DivePreferenceRead, DivePreferenceUpdate
from .diver_gear import DiverGearCreate, DiverGearRead, DiverGearUpdate

# 3. Import Primary Schemas After Dependencies
from .diver_profile import DiverProfileCreate, DiverProfileCreateResponse, DiverProfileRead, DiverProfileUpdate

# 4. Import Response Schemas Last
from .diver_info_response import DiverInfoResponse, DiverInfoData

from .favorite_marine_life import FavoriteMarineLifeCreate, FavoriteMarineLifeCreateMultiple, FavoriteMarineLifeRead, FavoriteMarineLifeUpdate

from .onboarding_profile import OnboardingProfileCreate, OnboardingProfileRead, OnboardingProfileUpdate, OnboardingProfileCreateRequest
from .master_love_to import MasterLoveToCreate, MasterLoveToRead, MasterLoveToUpdate
from .master_previous_dive_site import MasterPreviousDiveSiteCreate, MasterPreviousDiveSiteRead
from .profile_love_to import ProfileLoveToCreate, ProfileLoveToRead, ProfileLoveToUpdate
from .profile_previous_dive_site import ProfilePreviousDiveSiteCreate, ProfilePreviousDiveSiteRead, ProfilePreviousDiveSiteUpdate

# 5. Print Statements for Debugging (Optional)
print("Imported Master schemas")
print("Imported DiverLicense schemas")
print("Imported DivePreference schemas")
print("Imported DiverGear schemas")
print("Imported DiverProfile schemas")
print("Imported DiverInfoResponse schemas")

# 6. No Need to Resolve Forward References Manually in Pydantic v2
# Pydantic v2 handles forward references automatically with postponed evaluation