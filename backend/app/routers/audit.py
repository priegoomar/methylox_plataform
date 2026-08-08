from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog
from app.security import get_current_user_claims

router = APIRouter(prefix="/api/v1/audit", tags=["Audit Trail"])

# ============================================================
# GET AUDIT TRAIL
# ============================================================

@router.get("/")
def get_audit_logs(db: Session = Depends(get_db), current_user = Depends(get_current_user_claims)):
    """
    Returns the complete audit trail.

    Only administrators can access the audit trail.
    Results are ordered from newest to oldest.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()

    return [
        {
            "id": log.id,
            "user_id": log.user_id,
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
        for log in logs
    ]

# ============================================================
# GET SINGLE AUDIT EVENT
# ============================================================

@router.get("/{audit_id}")
def get_audit_event(audit_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user_claims)):
    """
    Returns a single audit event.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    log = db.query(AuditLog).filter(AuditLog.id == audit_id).first()

    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit event not found")

    return {
        "id": log.id,
        "user_id": log.user_id,
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
