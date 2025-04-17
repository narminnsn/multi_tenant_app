from app.tenants.models import TenantUser
from tortoise import Tortoise
from fastapi import HTTPException

# TENANT_DB_TEMPLATE = "postgres://user:password@localhost:5432/tenant_{}"


class TenantUserRepository:
    async def create_user(self, **kwargs):
        user = await TenantUser.create(**kwargs)
        return user

    async def get_user_by_id(self, user_id: int):
        return await TenantUser.get(id=user_id)

    async def edit_user_by_id(self, id: int, **profile):
        user = await TenantUser.filter(id=id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.username = profile["username"]
        user.email = profile["email"]
        await user.save()
        return user
