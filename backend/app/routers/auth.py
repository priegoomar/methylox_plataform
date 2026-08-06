from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.security import create_access_token
from app.utils.password import verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.active:
        raise HTTPException(status_code=403, detail="User inactive")

    user.last_login = datetime.now(timezone.utc)
    db.commit()

    token = create_access_token({
        "sub": user.username,
        "id_user": user.id,
        "role": user.role,
        "id_hospital": user.hospital_id,
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username,
        "hospital_id": user.hospital_id,
    }
