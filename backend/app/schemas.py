from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr, ConfigDict


# ==========================================
# AUTH / USER SCHEMAS
# ==========================================

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "viewer"


class UserCreate(UserBase):
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PermissionResponse(BaseModel):
    id: int
    name: str
    module: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    id: int
    active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    permissions: List[PermissionResponse] = []

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# PATIENT SCHEMAS
# ==========================================

class PatientBase(BaseModel):
    patient_code: str
    demographics: Optional[Dict[str, Any]] = None
    clinical_notes: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# SAMPLE / LIMS SCHEMAS
# ==========================================

class SampleBase(BaseModel):
    sample_code: str
    patient_id: int
    sample_type: str
    collection_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    status: Optional[str] = "Collected"
    storage_location: Optional[str] = None


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

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# ANALYSIS SCHEMAS
# ==========================================

class AnalysisCreate(BaseModel):
    sample_id: int
    pipeline_version: Optional[str] = "METHYLOX Analysis v1.0"
    qc_status: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    classification: Optional[str] = None


class AnalysisResponse(AnalysisCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# AUDIT SCHEMAS
# ==========================================

class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    module: str
    entity: Optional[str]
    changes: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# ACCESS CONTROL SCHEMAS
# ==========================================

class PermissionCreate(BaseModel):
    name: str
    module: str
    description: Optional[str] = None


class UserPermissionCreate(BaseModel):
    user_id: int
    permission_id: int
    granted_by: Optional[int] = None


class UserPermissionResponse(BaseModel):
    id: int
    user_id: int
    permission_id: int
    granted_by: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
