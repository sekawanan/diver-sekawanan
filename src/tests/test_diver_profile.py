# app/tests/test_diver_profile.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.database.session import get_db, Base, engine
from app.models.diver_profile import DiverProfile

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
async def test_create_diver_profile(client: AsyncClient):
    response = await client.post(
        "/api-lab/v1/diver-profiles",
        json={
            "user_id": 1,
            "first_name": "Johan",
            "last_name": "Sianipar"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Johan"
    assert data["last_name"] == "Sianipar"

@pytest.mark.asyncio
async def test_read_diver_profiles(client: AsyncClient):
    response = await client.get("/api-lab/v1/diver-profiles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["first_name"] == "Johan"

@pytest.mark.asyncio
async def test_read_diver_profile(client: AsyncClient):
    response = await client.get("/api-lab/v1/diver-profiles/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["first_name"] == "Johan"

@pytest.mark.asyncio
async def test_update_diver_profile(client: AsyncClient):
    response = await client.put(
        "/api-lab/v1/diver-profiles/1",
        json={
            "first_name": "Jonathan"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jonathan"

@pytest.mark.asyncio
async def test_delete_diver_profile(client: AsyncClient):
    response = await client.delete("/api-lab/v1/diver-profiles/1")
    assert response.status_code == 204

    # Verify deletion
    response = await client.get("/api-lab/v1/diver-profiles/1")
    assert response.status_code == 404