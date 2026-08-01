from app.security import create_access_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose
from app.database import get_db
from app.config import settings
from app import models, schemas


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==========================================
# PASSWORD SECURITY
# ==========================================

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ==========================================
# CREATE USER
# ==========================================

@router.post("/provision-user", response_model=schemas.UserResponse)
def provision_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ==========================================
# LOGIN
# ==========================================

@router.post("/login", response_model=schemas.Token)
def login(
    credentials: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.username == credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not user.active:
        raise HTTPException(
            status_code=403,
            detail="User inactive"
        )

    user.last_login = datetime.utcnow()
    db.commit()

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
