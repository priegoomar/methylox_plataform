from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/api/v1/access",
    tags=["Access Control"]
)


# ==========================================
# CREATE PERMISSION
# ==========================================

@router.post(
    "/permissions",
    response_model=schemas.PermissionResponse
)
def create_permission(
    permission: schemas.PermissionCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(models.Permission)
        .filter(
            models.Permission.name ==
            permission.name
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Permission already exists"
        )

    new_permission = models.Permission(
        name=permission.name,
        module=permission.module,
        description=permission.description
    )

    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)

    return new_permission


# ==========================================
# ASSIGN PERMISSION TO USER
# ==========================================

@router.post(
    "/assign",
    response_model=schemas.UserPermissionResponse
)
def assign_permission(
    data: schemas.UserPermissionCreate,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(
            models.User.id ==
            data.user_id
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    permission = (
        db.query(models.Permission)
        .filter(
            models.Permission.id ==
            data.permission_id
        )
        .first()
    )

    if not permission:
        raise HTTPException(
            status_code=404,
            detail="Permission not found"
        )

    new_assignment = models.UserPermission(
        user_id=data.user_id,
        permission_id=data.permission_id,
        granted_by=data.granted_by
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment


# ==========================================
# GET USER PERMISSIONS
# ==========================================

@router.get(
    "/user/{user_id}"
)
def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db)
):
    permissions = (
        db.query(models.Permission)
        .join(
            models.UserPermission
        )
        .filter(
            models.UserPermission.user_id ==
            user_id
        )
        .all()
    )

    return permissions
