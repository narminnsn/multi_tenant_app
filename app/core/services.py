from fastapi import HTTPException
from app.core.repository import UserRepository, OrganizationRepository
from app.core.events import EventDispatcher
from app.core.listeners import UserRegisteredListener, OrganizationCreatedListener
from app.core.models import User
from app.tenants.services import TenantProvisioningService
from app.auth.jwt import create_access_token, hash_password, verify_password
from datetime import timedelta
from tortoise import Tortoise

EventDispatcher.register("user_registered", UserRegisteredListener())
EventDispatcher.register("organization_created", OrganizationCreatedListener())


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def register_user(self, username: str, password: str):
        existing = await User.filter(username=username).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        user = await User.create(
            username=username, hashed_password=hash_password(password)
        )
        return user

    async def authenticate_user(self, username: str, password: str):
        user = await User.filter(username=username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token_data = {"sub": str(user.id), "scope": "core"}
        token = create_access_token(token_data, timedelta(minutes=60))

        return {"access_token": token, "token_type": "bearer"}


class OrganizationService:
    def __init__(self):
        self.org_repo = OrganizationRepository()

    async def create_organization(self, name: str, owner: User):
        try:
            org = await self.org_repo.create(name=name, owner=owner)
            EventDispatcher.dispatch("organization_created", {"name": name})
            success = await TenantProvisioningService.create_tenant_database(org.id)

            if not success:
                raise Exception("Failed to create tenant database")
            return org
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during organization creation: {str(e)}"
            )
