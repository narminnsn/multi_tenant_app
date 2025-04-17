import pytest


@pytest.mark.asyncio
async def test_core_register(client):
    response = await client.post(
        "/api/auth/register",
        json={
            "username": "coreuser",
            "email": "coreuser@example.com",
            "password": "password",
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_core_login(client):
    response = await client.post(
        "/api/auth/login", json={"username": "coreuser", "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_create_organization(client):
    login = await client.post(
        "/api/auth/login", json={"username": "coreuser", "password": "password"}
    )
    token = login.json()["access_token"]

    response = await client.post(
        "/api/organizations",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Tenant B"},
    )
    print("PRINTTTT", response.json())

    assert response.status_code == 200
    assert "organization_id" in response.json()
