from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import create_access_token
from app.utils.password import verify_password


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

# ============================================================================
# NOTA DE SEGURIDAD (corrección aplicada):
#
# Este archivo tenía un endpoint POST /provision-user SIN NINGUNA protección
# de autenticación ni de rol. Cualquiera con la URL, sin token, podía crear
# un usuario con role="admin" y tomar control administrativo del sistema.
#
# La creación de usuarios ya existe, correctamente protegida con
# check_admin(), en app/routers/users.py -> POST /api/v1/users/.
# Por eso ese endpoint se retiró de aquí. El frontend debe apuntar a
# POST /api/v1/users/ (requiere estar autenticado como admin).
#
# Este router ahora solo maneja login, que es lo que le corresponde.
# ============================================================================


# ==========================================
# LOGIN OAuth2
# ==========================================

@router.post(
    "/login",
    response_model=schemas.Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(
            models.User.username == form_data.username
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not user.active:
        raise HTTPException(
            status_code=403,
            detail="User inactive"
        )

    user.last_login = datetime.now(timezone.utc)
    db.commit()

    token = create_access_token(
        {
            "sub": user.username,
            "id_user": user.id,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username
    }
