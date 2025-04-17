from fastapi import HTTPException
from app.core.services import UserService
from app.config import settings
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext


class TenantAuthService:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.user_service = UserService()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(
        self, user_id: int, expires_delta: timedelta = timedelta(minutes=15)
    ):
        try:
            to_encode = {"sub": str(user_id), "tenant_id": self.tenant_id}
            expire = datetime.utcnow() + expires_delta
            encoded_jwt = jwt.encode(
                to_encode,
                settings.JWT_SECRET_KEY,
                algorithm=settings.JWT_ALGORITHM,
                expires_at=expire,
            )
            return encoded_jwt
        except JWTError as e:
            raise HTTPException(
                status_code=500, detail=f"JWT creation failed: {str(e)}"
            )

    async def authenticate_user(self, email: str, password: str):
        try:
            user = await self.user_service.authenticate_user(email, password)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            return self.create_access_token(user.id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error during authentication in tenant: {str(e)}",
            )
