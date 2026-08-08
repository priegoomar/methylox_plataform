from datetime import datetime, timedelta, timezone
from typing import List

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app import models


# ============================================================
# JWT CONFIGURATION
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


# ============================================================
# TOKEN DATA
# ============================================================

class TokenData(BaseModel):
    id_user: int
    username: str
    role: str
    id_hospital: int | None = None


# ============================================================
# CREATE ACCESS TOKEN
# ============================================================

def create_access_token(data: dict):
    """
    Creates a signed JWT containing the authenticated
    user's identity and authorization claims.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expire
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ============================================================
# CURRENT AUTHENTICATED USER
# ============================================================

def get_current_user_claims(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Validates the JWT and then validates the user against
    the current database state.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        id_user = payload.get("id_user")
        role = payload.get("role")
        id_hospital = payload.get("id_hospital")

        if not username or id_user is None or not role:
            raise credentials_exception

        try:
            id_user = int(id_user)
        except (TypeError, ValueError):
            raise credentials_exception

        user = db.query(models.User).filter(models.User.id == id_user).first()
        if not user:
            raise credentials_exception

        if user.active is not True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        if user.username != username or user.role != role or user.hospital_id != id_hospital:
            raise credentials_exception

        if user.hospital_id is not None:
            hospital = db.query(models.Hospital).filter(models.Hospital.id == user.hospital_id).first()
            if not hospital:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Hospital account not found"
                )
            if hospital.active is not True:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Hospital account is inactive"
                )

        return TokenData(
            id_user=user.id,
            username=user.username,
            role=user.role,
            id_hospital=user.hospital_id
        )

    except HTTPException:
        raise
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise credentials_exception
    except Exception as error:
        print("AUTHENTICATION ERROR:", str(error))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error"
        )


# ============================================================
# ROLE GUARD
# ============================================================

class RoleGuard:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: TokenData = Depends(get_current_user_claims)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user


# ============================================================
# PERMISSION GUARD
# ============================================================

class PermissionGuard:
    def __init__(self, permission_name: str):
        self.permission_name = permission_name

    def __call__(
        self,
        current_user: TokenData = Depends(get_current_user_claims),
        db: Session = Depends(get_db)
    ):
        if current_user.role == "admin":
            return current_user

        permission = (
            db.query(models.Permission)
            .join(
                models.UserPermission,
                models.Permission.id == models.UserPermission.permission_id
            )
            .filter(
                models.UserPermission.user_id == current_user.id_user,
                models.Permission.name == self.permission_name
            )
            .first()
        )

        if permission is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {self.permission_name}"
            )

        return current_user
