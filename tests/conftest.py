from httpx import AsyncClient
import pytest


@pytest.fixture
async def client():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client
