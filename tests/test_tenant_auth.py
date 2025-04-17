import pytest

TENANT = "1"


@pytest.fixture
async def tenant_token(client):
    response = await client.post(
        "/api/auth/login",
        headers={"X-TENANT": TENANT},
        json={"username": "newuser", "password": "password"},
    )
    assert response.status_code == 200
    tenant_token = response.json().get("access_token")
    assert tenant_token is not None
    return tenant_token


@pytest.mark.asyncio
async def test_tenant_register(client):
    response = await client.post(
        "/api/auth/register",
        headers={"X-TENANT": "3"},
        json={
            "username": "newuser",
            "email": "tenantuser@example.com",
            "password": "password",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User registered in tenant successfully."}


@pytest.mark.asyncio
async def test_tenant_login(client):
    response = await client.post(
        "/api/auth/login",
        headers={"X-TENANT": TENANT},
        json={"username": "newuser", "password": "password"},
    )
    print("PRINTTT", response.json())

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_user_profile(client, tenant_token):
    response = await client.get(
        "/api/users/me",
        headers={"X-TENANT": TENANT, "Authorization": f"Bearer {tenant_token}"},
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_user_profile(client, tenant_token):
    response = await client.put(
        "/api/users/me",
        headers={"X-TENANT": TENANT, "Authorization": f"Bearer {tenant_token}"},
        json={"username": "updatedname", "email": "updatedemail@example.com"},
    )
    print("PRINTTTr=teT", response.json())

    assert response.status_code == 200
