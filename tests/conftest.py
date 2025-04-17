from httpx import AsyncClient
import pytest
from app.main import app  # FastAPI uygulamanız


@pytest.fixture
async def client():
    # app'i parametre olarak geçmek yerine sadece base_url ayarlıyoruz
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client
