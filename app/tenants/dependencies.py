from fastapi import HTTPException, Request, Header
from app.tenants.services import TenantUserService, TenantProvisioningService
from tortoise import Tortoise, connections
from typing import Optional
from app.config.settings import settings


async def get_tenant_db(x_tenant: Optional[str] = Header(None)):
    if not x_tenant:
        return None
    db_url = f"{settings.DATABASE_URL}_{x_tenant}"

    try:
        await Tortoise.init(
            db_url=db_url, modules={"models": ["app.tenants.models"]}, _create_db=False
        )
        db = connections.get("default")

        return db
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error connecting to tenant database: {str(e)}"
        )
