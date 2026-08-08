from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import RoleGuard, TokenData
from app.utils.audit import create_audit_log


router = APIRouter(prefix="/api/v1/access", tags=["Access Control"])


# ============================================================
# ADMIN CHECK
# ============================================================

def check_admin(current_user: TokenData):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )


# ============================================================
# HOSPITAL ACCESS CHECK
# ============================================================

def check_user_hospital(user, current_user: TokenData):
    """
    Prevents an administrator from managing users
    belonging to another hospital.
    """
    if user.hospital_id != current_user.id_hospital:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hospital access denied"
        )


# ============================================================
# CREATE PERMISSION
# ============================================================

@router.post("/permissions", response_model=schemas.PermissionResponse)
def create_permission(
    permission: schemas.PermissionCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(RoleGuard(["admin"]))
):
    existing = db.query(models.Permission).filter(models.Permission.name == permission.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")

    new_permission = models.Permission(
        name=permission.name,
        module=permission.module,
        description=permission.description
    )

    try:
        db.add(new_permission)
        db.commit()
        db.refresh(new_permission)

        create_audit_log(
            db=db,
            user_id=current_user.id_user,
            action="CREATE_PERMISSION",
            module="access_control",
            entity=str(new_permission.id),
            changes={
                "name": new_permission.name,
                "module": new_permission.module
            }
        )

        return new_permission
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create permission")


# ============================================================
# ASSIGN PERMISSION
# ============================================================

@router.post("/assign", response_model=schemas.UserPermissionResponse)
def assign_permission(
    data: schemas.UserPermissionCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(RoleGuard(["admin"]))
):
    user = db.query(models.User).filter(models.User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    check_user_hospital(user, current_user)

    permission = db.query(models.Permission).filter(models.Permission.id == data.permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    existing_assignment = db.query(models.UserPermission).filter(
        models.UserPermission.user_id == data.user_id,
        models.UserPermission.permission_id == data.permission_id
    ).first()

    if existing_assignment:
        raise HTTPException(status_code=400, detail="Permission already assigned")

    new_assignment = models.UserPermission(
        user_id=data.user_id,
        permission_id=data.permission_id,
        granted_by=current_user.id_user
    )

    try:
        db.add(new_assignment)
        db.commit()
        db.refresh(new_assignment)

        create_audit_log(
            db=db,
            user_id=current_user.id_user,
            action="ASSIGN_PERMISSION",
            module="access_control",
            entity=str(user.id),
            changes={
                "username": user.username,
                "permission": permission.name,
                "permission_id": permission.id
            }
        )

        return new_assignment
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not assign permission")


# ============================================================
# GET USER PERMISSIONS
# ============================================================

@router.get("/user/{user_id}")
def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(RoleGuard(["admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    check_user_hospital(user, current_user)

    permissions = db.query(models.Permission).join(models.UserPermission).filter(
        models.UserPermission.user_id == user_id
    ).all()

    return permissions


# ============================================================
# GET ALL PERMISSIONS
# ============================================================

@router.get("/permissions")
def get_permissions(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(RoleGuard(["admin"]))
):
    return db.query(models.Permission).all()


# ============================================================
# REVOKE PERMISSION
# ============================================================

@router.delete("/revoke")
def revoke_permission(
    user_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(RoleGuard(["admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    check_user_hospital(user, current_user)

    assignment = db.query(models.UserPermission).filter(
        models.UserPermission.user_id == user_id,
        models.UserPermission.permission_id == permission_id
    ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Permission assignment not found")

    permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
    permission_name = permission.name if permission else str(permission_id)

    try:
        db.delete(assignment)
        db.commit()

        create_audit_log(
            db=db,
            user_id=current_user.id_user,
            action="REVOKE_PERMISSION",
            module="access_control",
            entity=str(user.id),
            changes={
                "username": user.username,
                "permission": permission_name,
                "permission_id": permission_id
            }
        )

        return {"message": "Permission revoked successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not revoke permission")
