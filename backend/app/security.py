from datetime import datetime, timedelta, timezone
from typing import List

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.database import get_db


# ==========================================
# OAUTH2 JWT CONFIGURATION
# ==========================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


# ==========================================
# TOKEN DATA MODEL
# ==========================================

class TokenData(BaseModel):
    id_user: int
    username: str
    role: str
    id_hospital: int | None = None


# ==========================================
# CREATE JWT TOKEN
# ==========================================

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ==========================================
# CURRENT USER FROM TOKEN
# ==========================================

async def get_current_user_claims(
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        id_user = payload.get("id_user")
        role = payload.get("role")
        id_hospital = payload.get("id_hospital")

        if username is None:
            raise credentials_exception

        return TokenData(
            id_user=id_user,
            username=username,
            role=role,
            id_hospital=id_hospital
        )

    except jwt.PyJWTError:
        raise credentials_exception


# ==========================================
# ROLE GUARD
# ==========================================

class RoleGuard:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        current_user: TokenData = Depends(get_current_user_claims)
    ):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )
        return current_user


# ==========================================
# PERMISSION GUARD
# ==========================================

class PermissionGuard:
    def __init__(self, permission_name: str):
        self.permission_name = permission_name

    def __call__(
        self,
        current_user: TokenData = Depends(get_current_user_claims),
        db: Session = Depends(get_db)
    ):
        # ADMIN BYPASS
        if current_user.role == "admin":
            return current_user

        permission = (
            db.query(models.Permission)
            .join(models.UserPermission)
            .filter(
                models.UserPermission.user_id == current_user.id_user,
                models.Permission.name == self.permission_name
            )
            .first()
        )

        if not permission:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user
