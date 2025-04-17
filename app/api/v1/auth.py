from fastapi import APIRouter, HTTPException, Header, Depends
from app.core.services import UserService
from pydantic import BaseModel
from typing import Optional
from app.tenants.models import TenantUser
from app.tenants.dependencies import get_tenant_db
from app.tenants.services import TenantUserService

router = APIRouter()
user_service = UserService()


class UserRegister(BaseModel):
    username: str
    password: str
    email: str


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(
    user: UserRegister,
    x_tenant: Optional[str] = Header(None),
    db=Depends(get_tenant_db),
):
    try:
        if x_tenant is None:
            created_user = await user_service.register_user(
                user.username, user.password
            )
            return {"message": "User registered successfully."}
        else:
            print("else")
            tenant_user_service = TenantUserService(tenant_id=x_tenant)
            tenant_user = await tenant_user_service.register_user(
                username=user.username, password=user.password, email=user.email, db=db
            )
            return {"message": "User registered in tenant successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed:{e}")


@router.post("/login")
async def login(
    user: UserLogin, x_tenant: Optional[str] = Header(None), db=Depends(get_tenant_db)
):
    try:
        if x_tenant is None:
            authenticated_user = await user_service.authenticate_user(
                user.username, user.password
            )
            if authenticated_user:
                return {
                    "access_token": authenticated_user["access_token"],
                    "message": "Login successful.",
                }
        elif x_tenant:
            tenant_user_service = TenantUserService(tenant_id=x_tenant)
            authenticated_user = await tenant_user_service.authenticate_user(
                user.username, user.password, db=db
            )
            if authenticated_user:
                return {
                    "access_token": authenticated_user["access_token"],
                    "message": "Login successful.",
                }
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed:{e}")
