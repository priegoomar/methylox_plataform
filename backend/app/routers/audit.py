from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog
from app.security import get_current_user_claims

router = APIRouter(
    prefix="/api/v1/audit",
    tags=["Audit"]
)


# ============================================================
# GET AUDIT LOGS
# ============================================================

@router.get("/")
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_claims)
):
    # Only administrators can access the audit trail
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    logs = (
        db.query(AuditLog)
        .filter(
            AuditLog.user_id.in_(
                db.query(
                    __import__("app.models", fromlist=["User"]).User.id
                ).filter(
                    __import__("app.models", fromlist=["User"]).User.hospital_id
                    == current_user.id_hospital
                )
            )
        )
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    return logs
