from fastapi import APIRouter, HTTPException, Depends
from app.tenants.models import TenantUser
from app.tenants.repositories import TenantUserRepository
from pydantic import BaseModel
from app.auth.auth_bearer import JWTBearer
from app.core.dependencies import get_current_user
from app.tenants.dependencies import get_tenant_db
from app.auth.jwt import decode_access_token

router = APIRouter()


@router.get("/users/me")
async def get_me(token: str = Depends(JWTBearer()), db=Depends(get_tenant_db)):
    try:
        tenant_repository = TenantUserRepository()
        user_id = decode_access_token(token)
        user = await tenant_repository.get_user_by_id(user_id=user_id["sub"])
        return {"id": user.id, "name": user.username, "email": user.email}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error during organization creation: {str(e)}"
        )


class UpdateUserProfile(BaseModel):
    username: str
    email: str


@router.put("/users/me")
async def update_me(
    profile: UpdateUserProfile,
    token: str = Depends(JWTBearer()),
    db=Depends(get_tenant_db),
):
    tenant_repository = TenantUserRepository()
    user_id = decode_access_token(token)
    user = await tenant_repository.edit_user_by_id(
        user_id["sub"], **profile.model_dump()
    )
    return {"id": user.id, "username": user.username, "email": user.email}
