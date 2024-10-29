# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os
from dotenv import load_dotenv  # Ensure environment variables are loaded

# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add the app directory to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

# Import your models and Base
from app.models import (
    DiverProfile, DiverLicense, MasterLicense, MasterDivePreference,
    DivePreference, MasterDiveSite, MasterGear, MasterBrand, MasterGearBrand, 
    DiverAdditionalData, MasterColor, MasterMarineLife, MasterDiveType, DiveLog, DiverGear, FavoriteMarineLife,
    MasterLoveTo, MasterPreviousDiveSite, OnboardingProfile, ProfileLoveTo, ProfilePreviousDiveSite, User
)
from app.database.session import Base
from app.core.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# set the target metadata for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL_SYNC
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {
            "sqlalchemy.url": settings.DATABASE_URL_SYNC
        },
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Optional: to detect column type changes
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()