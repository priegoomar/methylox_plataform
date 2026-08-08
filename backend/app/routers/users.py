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
# HOSPITAL ACCESS CHECK
# ============================================================

def check_hospital_access(user, current_user):
    """
    Ensures that an administrator can only manage
    users belonging to their own hospital.
    """
    if user.hospital_id != current_user.id_hospital:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hospital access denied"
        )


# ============================================================
# GET USERS
# ============================================================

@router.get("/")
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_claims)
):
    check_admin(current_user)
    users = db.query(models.User).filter(models.User.hospital_id == current_user.id_hospital).all()
    return [serialize_user(user) for user in users]


# ============================================================
# GET USER
# ============================================================

@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_claims)
):
    check_admin(current_user)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    check_hospital_access(user, current_user)
    return serialize_user(user)


# ============================================================
# CREATE USER
# ============================================================

@router.post("/")
def create_user(
    payload: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_claims)
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

    try:
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
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create user")


# ============================================================
# UPDATE USER
# ============================================================

@router.patch("/{user_id}")
def update_user(
    user_id: int,
    payload: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_claims)
):
    check_admin(current_user)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    check_hospital_access(user, current_user)
    changes = {}

    if payload.full_name is not None and payload.full_name != user.full_name:
        changes["full_name"] = {"old": user.full_name, "new": payload.full_name}
        user.full_name = payload.full_name

    if payload.email is not None and payload.email != user.email:
        if db.query(models.User).filter(models.User.email == payload.email, models.User.id != user.id).first():
            raise HTTPException(status_code=400, detail="Email already exists")
        changes["email"] = {"old": user.email, "new": payload.email}
        user.email = payload.email

    if payload.role is not None and payload.role != user.role:
        changes["role"] = {"old": user.role, "new": payload.role}
        user.role = payload.role

    try:
        db.commit()
        db.refresh(user)

        if changes:
            create_audit_log(
                db=db,
                user_id=current_user.id_user,
                action="UPDATE_USER",
                module="users",
                entity=str(user.id),
                changes=changes
            )

        return {
            "message": "User updated successfully",
            "user": serialize_user(user)
        }
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not update user")


# ============================================================
# CHANGE PASSWORD
# ============================================================

@router.patch("/{user_id}/password")
def change_user_password(
    user_id: int,
    payload: schemas.UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_claims)
):
    check_admin(current_user)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    check_hospital_access(user, current_user)
    user.password_hash = hash_password(payload.password)

    try:
        db.commit()

        create_audit_log(
            db=db,
            user_id=current_user.id_user,
            action="CHANGE_PASSWORD",
            module="users",
            entity=str(user.id),
            changes={"username": user.username}
        )

        return {"message": "Password changed successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not change password")


# ============================================================
# UPDATE STATUS
# ============================================================

@router.patch("/{user_id}/status")
def update_user_status(
    user_id: int,
    payload: schemas.UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_claims)
):
    check_admin(current_user)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    check_hospital_access(user, current_user)
    old_status = user.active

    if old_status == payload.active:
        return {"message": "User status unchanged", "active": user.active}

    user.active = payload.active

    try:
        db.commit()
        db.refresh(user)

        action = "ACTIVATE_USER" if payload.active else "DEACTIVATE_USER"

        create_audit_log(
            db=db,
            user_id=current_user.id_user,
            action=action,
            module="users",
            entity=str(user.id),
            changes={
                "username": user.username,
                "old_active": old_status,
                "new_active": user.active
            }
        )

        return {"message": "User status updated", "active": user.active}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not update user status")
