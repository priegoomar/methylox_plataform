from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import create_access_token
from app.utils.password import hash_password, verify_password


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

# ==========================================
# CREATE USER
# ==========================================

@router.post(
    "/provision-user",
    response_model=schemas.UserResponse
)
def provision_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(
            models.User.username == user.username
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ==========================================
# LOGIN OAuth2
# ==========================================

@router.post(
    "/login",
    response_model=schemas.Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(
            models.User.username == form_data.username
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not user.active:
        raise HTTPException(
            status_code=403,
            detail="User inactive"
        )

    user.last_login = datetime.utcnow()

    db.commit()

    token = create_access_token(
        {
            "sub": user.username,
            "id_user": user.id,
            "role": user.role,
            "id_hospital": user.
    id_hospital
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
