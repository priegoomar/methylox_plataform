from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.security import TokenData, PermissionGuard

# Asegúrate de que la variable se llame exactamente 'router'
router = APIRouter(
    prefix="/api/v1/audit",
    tags=["Audit Trail"]
)

@router.get("/", response_model=list[schemas.AuditLogResponse])
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(PermissionGuard("audit_read")) # O el permiso que corresponda
):
    return db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc()).all()
