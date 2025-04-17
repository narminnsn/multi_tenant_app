from app.core.models import User, Organization
from app.tenants.models import TenantUser
from tortoise.exceptions import DoesNotExist


class UserRepository:
    async def create(self, username: str, password: str):
        print("repo")
        user = await User.create(username=username, hashed_password=password)
        return user

    async def get_by_username(self, username: str):
        try:
            return await User.get(username=username)
        except DoesNotExist:
            return None


class OrganizationRepository:
    async def create(self, name: str, owner: User):
        org = await Organization.create(name=name, owner=owner)
        return org
