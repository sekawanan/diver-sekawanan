# app/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.exceptions import generic_exception_handler, http_exception_handler, validation_exception_handler
from app.core.jwt_manager import JWTManager
from app.api.v1.endpoints.diver_profile import api_router as diver_profile_router
from app.api.v1.endpoints.diver_license import api_router as diver_license_router
from app.api.v1.endpoints.diver_gear import api_router as diver_gear_router
from app.api.v1.endpoints.master_license import api_router as master_license_router
from app.api.v1.endpoints.master_dive_preference import api_router as master_dive_pref_router
from app.api.v1.endpoints.master_gear import api_router as master_gear_router
from app.api.v1.endpoints.master_brand import api_router as master_brand_router
from app.api.v1.endpoints.master_gear_brand import api_router as master_gear_brand_router
from app.api.v1.endpoints.master_dive_site import api_router as master_dive_site_router
from app.api.v1.endpoints.master_marine_life import api_router as master_marine_life_router
from app.api.v1.endpoints.dive_preference import api_router as dive_preference_router
from app.api.v1.endpoints.dive_log import api_router as dive_log_router
from app.api.v1.endpoints.master_dive_type import api_router as master_dive_type_router
from app.api.v1.endpoints.favorite_marine_life import api_router as favorite_marine_life_router
from app.api.v1.endpoints.onboarding_profile import api_router as onboarding_profile_router
from app.api.v1.endpoints.master_love_to import api_router as master_love_to_router
from app.api.v1.endpoints.master_previous_dive_site import api_router as master_previous_dive_site_router
from app.api.v1.endpoints.profile_love_to import api_router as profile_love_to_router
from app.api.v1.endpoints.profile_previous_dive_site import api_router as profile_previous_dive_site_router
from app.services.favorite_marine_life_service import DuplicateFavoriteMarineLifeError
from app.services.dive_preference_service import DuplicateDivePreferenceError
from app.core.config import settings
from app.database.session import engine, Base
from contextlib import asynccontextmanager
import logging
from sqlalchemy.exc import IntegrityError


# logging.basicConfig(level=logging.INFO)
# jwt_manager = JWTManager(secret_key=settings.SECRET_KEY, algorithm="HS256")

# Configure logging
# Configure logging
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
# Set up logging for SQLAlchemy to show SQL queries
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# logger = logging.getLogger(__name__)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.handlers.RotatingFileHandler("app.log", maxBytes=1000000, backupCount=5)

# Create formatters and add them to handlers
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Configure SQLAlchemy logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Initialize JWT Manager
jwt_manager = JWTManager(secret_key=settings.SECRET_KEY, algorithm="HS256")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown logic
    logger.info("Shutting down...")
    await engine.dispose()

# Create FastAPI instance with lifespan
app = FastAPI(
    title="Diver API",
    version="1.0.0",
    lifespan=lifespan,
    root_path="/api-lab",
    debug=True  # Enable debug mode
)


# Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,  # Define in your settings
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Include API routers
# app.include_router(diver_profile_router, prefix="/api-lab/v1", tags=["diver-profiles"])
# app.include_router(diver_license_router, prefix="/api-lab/v1", tags=["diver-licenses"])
# app.include_router(diver_gear_router, prefix="/api-lab/v1", tags=["diver-gears"])
# app.include_router(master_license_router, prefix="/api-lab/v1", tags=["master-licenses"])
# app.include_router(master_dive_pref_router, prefix="/api-lab/v1", tags=["master-dive-preferences"])
# app.include_router(master_gear_router, prefix="/v1/master-gears", tags=["master-gears"])
# app.include_router(master_brand_router, prefix="/v1/master-brands", tags=["master-brands"])
# app.include_router(master_gear_brand_router, prefix="/api-lab/v1", tags=["master-gears-brands"])
# app.include_router(master_color_router, prefix="/v1/master-colors", tags=["master-colors"])
# app.include_router(master_dive_site_router, prefix="/api-lab/v1", tags=["master-dive-sites"])
# app.include_router(master_marine_life_router, prefix="/api-lab/v1", tags=["master-marine-lifes"])
# app.include_router(dive_preference_router, prefix="/api-lab/v1", tags=["dive-preferences"])
# app.include_router(master_dive_type_router, prefix="/v1/dive-types", tags=["master-dive-types"])
# app.include_router(dive_log_router, prefix="/api-lab/v1", tags=["dive-logs"])
# app.include_router(favorite_marine_life_router, prefix="/v1/favorite-marine-life", tags=["Favorite Marine Life"])



# Include API routers with consistent prefixes and tags
app.include_router(
    diver_profile_router, 
    prefix="/v1", 
    tags=["Diver Profile"]
)
app.include_router(
    onboarding_profile_router, 
    prefix="/v1", 
    tags=["Onboarding Profiles"]
)
app.include_router(
    diver_gear_router, 
    prefix="/v1", 
    tags=["Diver Gear"]
)
app.include_router(
    diver_license_router, 
    prefix="/v1", 
    tags=["Diver License"]
)
app.include_router(
    master_brand_router, 
    prefix="/v1", 
    tags=["Master Brand"]
)
app.include_router(
    master_love_to_router, 
    prefix="/v1", 
    tags=["Master Love Tos"]
)
app.include_router(
    master_previous_dive_site_router, 
    prefix="/v1", 
    tags=["Master Previous Dive Sites"]
)
app.include_router(
    profile_love_to_router, 
    prefix="/v1", 
    tags=["Profile Love Tos"]
)
app.include_router(
    profile_previous_dive_site_router, 
    prefix="/v1", 
    tags=["Profile Previous Dive Sites"]
)

# app.include_router(user_router, prefix="/v1/authentication", tags=["User Authentication"])

@app.get("/health", status_code=200, tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    logger.info("Health check endpoint called.")
    return {"status": "healthy"}

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)