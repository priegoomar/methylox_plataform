from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog
from app.security import get_current_user_claims


router = APIRouter(prefix="/api/v1/audit", tags=["Audit Trail"])


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
# SERIALIZE AUDIT LOG
# ============================================================

def serialize_audit_log(log: AuditLog):
    return {
        "id": log.id,
        "user_id": log.user_id,
        "hospital_id": log.hospital_id,
        "action": log.action,
        "module": log.module,
        "entity": log.entity,
        "changes": log.changes,
        "ip_address": log.ip_address,
        "endpoint": log.endpoint,
        "http_method": log.http_method,
        "status_code": log.status_code,
        "created_at": log.created_at
    }


# ============================================================
# GET AUDIT TRAIL
# ============================================================

@router.get("/")
def get_audit_logs(db: Session = Depends(get_db), current_user = Depends(get_current_user_claims)):
    """
    Returns the audit trail for the administrator's hospital.

    Only administrators can access the audit trail.
    Results are ordered from newest to oldest.
    """
    check_admin(current_user)

    logs = (
        db.query(AuditLog)
        .filter(AuditLog.hospital_id == current_user.id_hospital)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    return [serialize_audit_log(log) for log in logs]


# ============================================================
# GET SINGLE AUDIT EVENT
# ============================================================

@router.get("/{audit_id}")
def get_audit_event(audit_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user_claims)):
    """
    Returns a single audit event.
    """
    check_admin(current_user)

    log = (
        db.query(AuditLog)
        .filter(
            AuditLog.id == audit_id,
            AuditLog.hospital_id == current_user.id_hospital
        )
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit event not found"
        )

    return serialize_audit_log(log)
