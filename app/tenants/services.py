from app.tenants.models import TenantUser

# from app.db import init_tenant_db
from passlib.context import CryptContext
from fastapi import HTTPException, Header
from tortoise import Tortoise
from app.auth.jwt import create_access_token, hash_password, verify_password
from datetime import timedelta
from app.config.settings import settings
from tortoise.transactions import in_transaction
import asyncpg

TENANT_DB_TEMPLATE = settings.DATABASE_URL


class TenantUserService:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register_user(self, username: str, password: str, email: str, db):
        # @staticmethod
        existing = await TenantUser.filter(username=username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Tenant user already exists")

        user = await TenantUser.create(
            username=username,
            hashed_password=hash_password(password),
            email=email,
        )

        return user

    async def authenticate_user(self, username: str, password: str, db):
        try:
            user = await TenantUser.filter(username=username).first()
            if not user or not verify_password(password, user.hashed_password):
                raise HTTPException(status_code=401, detail="Invalid credentials")

            token_data = {"sub": str(user.id), "scope": "core"}
            token = create_access_token(token_data, timedelta(minutes=60))

            return {"access_token": token, "token_type": "bearer"}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error during authentication in tenant: {str(e)}",
            )

    async def get_user_profile(self, user_id: int):
        try:
            user = await TenantUser.get(id=user_id, tenant_id=self.tenant_id)
            return user
        except Exception as e:
            raise HTTPException(
                status_code=404, detail=f"User not found in tenant: {str(e)}"
            )

    async def update_user_profile(self, user_id: int, username: str, email: str):
        try:
            user = await TenantUser.get(id=user_id, tenant_id=self.tenant_id)
            user.username = username
            user.email = email
            await user.save()
            return user
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error updating user profile in tenant: {str(e)}",
            )


class TenantProvisioningService:

    @staticmethod
    async def create_tenant_database(tenant_id: int):
        tenant_db_name = f"multi_tenant_database_{tenant_id}"
        connection_url = (
            "postgres://multi_tenant_user:zQhGyUUkeNov9SQ@localhost/postgres"
        )
        try:
            conn = await asyncpg.connect(
                "postgres://multi_tenant_user:zQhGyUUkeNov9SQ@localhost:5432/postgres"
            )

            create_db_query = f"CREATE DATABASE {tenant_db_name}"
            await conn.execute(create_db_query)

            await conn.close()

            tenant_db_url = f"postgres://multi_tenant_user:zQhGyUUkeNov9SQ@localhost:5432/{tenant_db_name}"

            await Tortoise.init(
                db_url=tenant_db_url,
                modules={"models": ["app.tenants.models"]},
                _create_db=False,
            )

            await Tortoise.generate_schemas()

            await Tortoise.close_connections()

            return {
                "status": "Tenant database created successfully",
                "db_url": tenant_db_url,
            }

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to create tenant database: {str(e)}"
            )
