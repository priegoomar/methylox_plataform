from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import get_current_user_claims
from app.utils.password import hash_password
from app.utils.audit import create_audit_log


router = APIRouter(prefix="/api/v1/users", tags=["Users"])


# ============================================================
# SERIALIZE USER
# ============================================================

def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "hospital_id": user.hospital_id,
        "active": user.active,
        "created_at": user.created_at,
        "last_login": user.last_login,
        "permissions": [
            {
                "id": p.id,
                "name": p.name,
                "module": p.module,
                "description": p.description
            }
            for p in user.direct_permissions
        ]
    }


# ============================================================
# ADMIN CHECK
# ============================================================

def check_admin(current_user):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )


# ============================================================
# GET USERS
# ============================================================

@router.get("/")
def get_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_claims)
):
    check_admin(current_user)
    query = db.query(models.User)

    if current_user.role != "admin":
        query = query.filter(models.User.hospital_id == current_user.id_hospital)

    return [serialize_user(u) for u in query.all()]


# ============================================================
# GET USER
# ============================================================

@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_claims)
):
    check_admin(current_user)
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.role != "admin" and user.hospital_id != current_user.id_hospital:
        raise HTTPException(status_code=403, detail="Hospital access denied")

    return serialize_user(user)


# ============================================================
# CREATE USER
# ============================================================

@router.post("/")
def create_user(
    payload: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_claims)
):
    check_admin(current_user)

    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        role=payload.role,
        hospital_id=current_user.id_hospital,
        password_hash=hash_password(payload.password),
        active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

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

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }


# ============================================================
# UPDATE USER
# ============================================================

@router.patch("/{user_id}")
def update_user(
    user_id: int,
    payload: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_claims)
):
    check_admin(current_user)
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.hospital_id != current_user.id_hospital:
        raise HTTPException(status_code=403, detail="Hospital access denied")

    if payload.full_name is not None:
        user.full_name = payload.full_name

    if payload.email is not None:
        user.email = payload.email

    if payload.role is not None:
        user.role = payload.role

    db.commit()

    return {
        "message": "User updated successfully"
    }


# ============================================================
# UPDATE STATUS
# ============================================================

@router.patch("/{user_id}/status")
def update_user_status(
    user_id: int,
    payload: schemas.UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_claims)
):
    check_admin(current_user)
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.hospital_id != current_user.id_hospital:
        raise HTTPException(status_code=403, detail="Hospital access denied")

    user.active = payload.active
    db.commit()

    return {
        "message": "User status updated",
        "active": user.active
    }
