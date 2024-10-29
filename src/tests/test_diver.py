# tests/test_diver.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.session import get_db
from app.models import Base

from app.core.config import settings

# Create a new database for testing
TEST_DATABASE_URL = "mysql+aiomysql://user:password@localhost:3306/test_db_name"

engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="session")
async def prepare_database():
    # Create the database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop the tables after tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(prepare_database):
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
def override_get_db(db_session):
    async def _get_db():
        yield db_session
    return _get_db

app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_read_license():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First, insert a diver and licenses into the test database
        diver = {
            "first_name": "John",
            "last_name": "Doe"
        }
        async with engine.begin() as conn:
            result = await conn.execute(
                DiverProfile.__table__.insert().values(**diver)
            )
            diver_id = result.inserted_primary_key[0]

            licenses = [
                {"diver_profile_id": diver_id, "master_license_id": 1, "certification_number": "CERT123"},
                {"diver_profile_id": diver_id, "master_license_id": 2, "certification_number": "CERT456"},
            ]
            await conn.execute(DiverLicense.__table__.insert(), licenses)

        # Now, test the API endpoint
        response = await ac.get(f"/api-lab/v1/diver-license?diver_profile_id={diver_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["first_name"] == "John"
        assert data["data"]["last_name"] == "Doe"
        assert len(data["data"]["licenses"]) == 2

        # Clean up (optional, since fixtures handle teardown)