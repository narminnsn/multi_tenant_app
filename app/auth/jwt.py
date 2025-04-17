from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
import logging
from app.core.models import User
from fastapi import HTTPException

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise JWTError("User ID not found in token")

        user = User.filter(id=user_id).first()
        if user is None:
            raise JWTError("User not found")

        return user
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid token or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str | None:
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Access token created successfully for: {data.get('sub')}")
        return token
    except Exception as e:
        logger.error(f"Error creating access token: {e}")
        return None


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        return None
