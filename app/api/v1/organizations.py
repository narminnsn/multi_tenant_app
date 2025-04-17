from fastapi import APIRouter, Depends, HTTPException
from app.core.services import OrganizationService
from app.core.dependencies import get_current_user
from app.core.models import User
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Annotated
from app.auth.auth_bearer import JWTBearer

router = APIRouter()


class OrganizationCreate(BaseModel):
    name: str


@router.post("/organizations")
async def create_organization(
    organization: OrganizationCreate, token: str = Depends(JWTBearer())
):
    try:
        organization_service = OrganizationService()
        user = await get_current_user(token)
        organization = await organization_service.create_organization(
            organization.name, user
        )
        # await organization_service.create_tenant_database(organization.id)

        return {"organization_id": organization.id, "name": organization.name}
    except HTTPException as e:
        raise HTTPException(
            status_code=500, detail=f"Error during organization creation: {str(e)}"
        )
    except Exception as e:
        raise Exception(status_code=500, detail=str(e))
