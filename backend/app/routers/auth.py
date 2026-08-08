from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import create_access_token, RoleGuard, TokenData
from app.utils.password import verify_password, hash_password
from app.utils.audit import create_audit_log


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=schemas.Token
)
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

    # --------------------------------------------------------
    # ACTIVE USER CHECK
    # --------------------------------------------------------

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
            detail="Login processing error"
        )


# ============================================================
# PROVISION USER
# ADMIN CREATES USER INSIDE HIS HOSPITAL
# ============================================================

@router.post(
    "/provision-user",
    response_model=schemas.UserResponse
)
def provision_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(
        RoleGuard(["admin"])
    )
):

    print(
        "PROVISION USER:",
        user_data.username
    )

    # --------------------------------------------------------
    # USERNAME
    # --------------------------------------------------------

    existing_username = (
        db.query(models.User)
        .filter(
            models.User.username == user_data.username
        )
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    existing_email = (
        db.query(models.User)
        .filter(
            models.User.email == user_data.email
        )
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # --------------------------------------------------------
    # CREATE USER
    # --------------------------------------------------------

    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        role=user_data.role,

        # IMPORTANT:
        # Hospital comes from authenticated admin,
        # NOT from client request.
        hospital_id=current_user.id_hospital,

        password_hash=hash_password(
            user_data.password
        ),

        active=True
    )

    try:

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        # ----------------------------------------------------
        # AUDIT
        # ----------------------------------------------------

        create_audit_log(
            db=db,
            user_id=current_user.id_user,
            action="CREATE_USER",
            module="users",
            entity=str(new_user.id),
            changes={
                "username": new_user.username,
                "role": new_user.role,
                "hospital_id": new_user.hospital_id
            }
        )

        print(
            "USER CREATED:",
            new_user.id
        )

        return new_user

    except Exception as e:

        db.rollback()

        print(
            "PROVISION USER ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Could not create user"
        )
