# app/tests/test_master_license.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.database.session import get_db, Base, engine
from app.models.master_license import MasterLicense

# Override the get_db dependency for testing
@pytest.fixture(scope="module")
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_session = AsyncSession(engine, expire_on_commit=False)
    try:
        yield async_session
    finally:
        await async_session.close()

@pytest.fixture(scope="module")
async def client(test_db: AsyncSession):
    async def override_get_db():
        yield test_db
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_read_master_licenses_empty(client: AsyncClient):
    response = await client.get("/api-lab/v1/master-licenses")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_create_master_license(client: AsyncClient, test_db: AsyncSession):
    # Since master_licenses only have GET methods, you should not have POST.
    # Ensure no POST route exists or return method not allowed.
    response = await client.post(
        "/api-lab/v1/master-licenses",
        json={
            "title": "Open Water",
            "type": "SSI",
            "issuer": "OW",
            "alias": "OpenWater"
        }
    )
    assert response.status_code == 405  # Method Not Allowed

@pytest.mark.asyncio
async def test_read_master_license(client: AsyncClient, test_db: AsyncSession):
    # Insert a master license directly into the database
    master_license = MasterLicense(
        id=1,
        title="Open Water",
        type="SSI",
        issuer="OW",
        alias="OpenWater"
    )
    test_db.add(master_license)
    await test_db.commit()

    response = await client.get("/api-lab/v1/master-licenses/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Open Water"
    assert data["type"] == "SSI"
    assert data["issuer"] == "OW"
    assert data["alias"] == "OpenWater"