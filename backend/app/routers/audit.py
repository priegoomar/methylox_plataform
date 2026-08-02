from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AuditLog
from app.security import get_current_user_claims

router = APIRouter()


@router.get("/")
def get_audit_logs(db: Session = Depends(get_db), current_user=Depends(get_current_user_claims)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
