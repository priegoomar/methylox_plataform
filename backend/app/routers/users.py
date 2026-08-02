from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.security import get_current_user_claims

router = APIRouter()


@router.get("/")
def get_users(db: Session = Depends(get_db), current_user=Depends(get_current_user_claims)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    users = db.query(User).all()
    response = []

    for user in users:
        permissions = [{"id": p.id, "name": p.name, "module": p.module, "description": p.description} for p in user.direct_permissions]
        response.append({
            "id": user.id, "username": user.username, "email": user.email,
            "full_name": user.full_name, "role": user.role, "active": user.active,
            "created_at": user.created_at, "last_login": user.last_login, "permissions": permissions
        })

    return response
