from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import create_access_token
from app.utils.password import verify_password


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


# ============================================================
# LOGIN
# ============================================================
@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    print("LOGIN ATTEMPT:", form_data.username)

    user = (
        db.query(models.User)
        .filter(
            models.User.username == form_data.username
        )
        .first()
    )


    if not user:
        print("USER NOT FOUND")
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    print("USER FOUND:", user.username)


    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        print("PASSWORD ERROR")
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    if not user.active:
        raise HTTPException(
            status_code=403,
            detail="User inactive"
        )


    try:

        user.last_login = datetime.now(timezone.utc)

        db.commit()


        token = create_access_token(
            {
                "sub": user.username,
                "id_user": user.id,
                "role": user.role,
                "id_hospital": user.hospital_id
            }
        )


        print("TOKEN CREATED")


        return {
            "access_token": token,
            "token_type": "bearer",
            "role": user.role,
            "username": user.username,
            "id_hospital": user.hospital_id
        }


    except Exception as e:

        print("LOGIN ERROR:", str(e))

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# PROVISION USER (ADMIN CREATES USERS)
# ============================================================

@router.post("/provision-user", response_model=schemas.UserResponse)
def provision_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        role=user_data.role,
        hospital_id=user_data.hospital_id,
        password_hash=user_data.password_hash,
        active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
    # ====================================================
    # JWT CON HOSPITAL
    # ====================================================

    token = create_access_token(
        {
            "sub": user.username,
            "id_user": user.id,
            "role": user.role,
            # NUEVO:
            # El usuario queda ligado
            # al hospital que pertenece
            "id_hospital": user.hospital_id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username,
        "id_hospital": user.hospital_id
    }
