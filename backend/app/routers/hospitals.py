from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.security import TokenData, get_current_user_claims

router = APIRouter(prefix="/api/v1/hospitals", tags=["Hospitals"])

@router.get("/me")
def get_my_hospital(db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user_claims)):
    hospital = db.query(models.Hospital).filter(models.Hospital.id == current_user.id_hospital).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return {"id": hospital.id, "name": hospital.name, "active": hospital.active}
