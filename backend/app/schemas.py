from datetime import datetime
from typing import Optional, Dict, Any, List

from pydantic import BaseModel, EmailStr, ConfigDict


# ============================================================
# HOSPITAL SCHEMAS
# ============================================================

class HospitalBase(BaseModel):
    name: str
    code: str


class HospitalCreate(HospitalBase):
    pass


class HospitalResponse(HospitalBase):
    id: int
    active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# AUTH / USER SCHEMAS
# ============================================================

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    hospital_id: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    hospital_id: Optional[int] = None


class UserStatusUpdate(BaseModel):
    active: bool


class UserPasswordUpdate(BaseModel):
    password: str
