from datetime import datetime
from typing import Optional, Dict, Any, List

from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
    Field
)


# ============================================================
# HOSPITAL
# ============================================================

class HospitalBase(BaseModel):
    name: str
    code: Optional[str] = None


class HospitalCreate(HospitalBase):
    pass


class HospitalResponse(HospitalBase):
    id: int
    active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# USER
# ============================================================

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    hospital_id: Optional[int] = None


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128
    )


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None

    # Kept for backward compatibility.
    # Server NEVER trusts this value when updating users.
    hospital_id: Optional[int] = None


class UserStatusUpdate(BaseModel):
    active: bool


class UserPasswordUpdate(BaseModel):
    password: str = Field(
        min_length=8,
        max_length=128
    )


# ============================================================
# TOKEN
# ============================================================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str
    id_hospital: Optional[int] = None


# ============================================================
# PERMISSIONS
# ============================================================

class PermissionResponse(BaseModel):
    id: int
    name: str
    module: str
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


class PermissionCreate(BaseModel):
    name: str
    module: str
    description: Optional[str] = None


class UserPermissionCreate(BaseModel):
    user_id: int
    permission_id: int


class UserPermissionResponse(BaseModel):
    id: int
    user_id: int
    permission_id: int
    granted_by: Optional[int]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# USER RESPONSE
# ============================================================

class UserResponse(UserBase):
    id: int
    active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    permissions: List[PermissionResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# PATIENTS
# ============================================================

class PatientBase(BaseModel):
    patient_code: str
    demographics: Optional[Dict[str, Any]] = None
    clinical_notes: Optional[str] = None
    hospital_id: Optional[int] = None


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class PatientCreate(PatientBase): pass

class PatientUpdate(BaseModel):
    demographics: Optional[Dict[str, Any]] = None
    clinical_notes: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# ============================================================
# SAMPLES / LIMS
# ============================================================

class SampleBase(BaseModel):
    sample_code: str
    patient_id: int
    sample_type: str
    collection_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    status: Optional[str] = "Collected"
    storage_location: Optional[str] = None
    hospital_id: Optional[int] = None


class SampleCreate(SampleBase):
    pass


class SampleUpdate(BaseModel):
    status: Optional[str] = None
    storage_location: Optional[str] = None
    received_date: Optional[datetime] = None


class SampleResponse(SampleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# ANALYSIS
# ============================================================

class AnalysisCreate(BaseModel):
    sample_id: int
    pipeline_version: Optional[str] = (
        "METHYLOX Analysis v1.0"
    )
    qc_status: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    classification: Optional[str] = None
    hospital_id: Optional[int] = None


class AnalysisResponse(AnalysisCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# AUDIT TRAIL
# ============================================================

class AuditLogResponse(BaseModel):
    id: int

    user_id: Optional[int] = None
    hospital_id: Optional[int] = None

    action: str
    module: str
    entity: Optional[str] = None

    changes: Optional[Dict[str, Any]] = None

    ip_address: Optional[str] = None
    endpoint: Optional[str] = None
    http_method: Optional[str] = None
    status_code: Optional[int] = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
