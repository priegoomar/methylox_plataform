from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserResponse
from app.security import get_current_user_claims


router = APIRouter()


# ==========================================
# USER MANAGEMENT
# ==========================================

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_claims)
):
    # Solo administrador puede consultar usuarios
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    users = (
        db.query(User)
        .all()
    )

    return users
