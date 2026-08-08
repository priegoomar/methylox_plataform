from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# ==========================================================
# HOSPITAL
# ==========================================================

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="hospital")
    patients = relationship("Patient", back_populates="hospital")
    samples = relationship("Sample", back_populates="hospital")
    analysis_results = relationship("AnalysisResult", back_populates="hospital")
    audit_logs = relationship("AuditLog", back_populates="hospital")


# ==========================================================
# USERS
# ==========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=True)
    role = Column(String(50), default="viewer")
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    hospital = relationship("Hospital", back_populates="users")
    permissions = relationship(
        "UserPermission",
        foreign_keys="UserPermission.user_id",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    direct_permissions = relationship(
        "Permission",
        secondary="user_permissions",
        primaryjoin="User.id==UserPermission.user_id",
        secondaryjoin="Permission.id==UserPermission.permission_id",
        viewonly=True
    )


# ==========================================================
# PATIENTS
# ==========================================================

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_code = Column(String(100), unique=True, nullable=False, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    demographics = Column(JSON, nullable=True)
    clinical_notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    hospital = relationship("Hospital", back_populates="patients")
    samples = relationship("Sample", back_populates="patient", cascade="all, delete-orphan")


# ==========================================================
# SAMPLES
# ==========================================================

class Sample(Base):
    __tablename__ = "samples"

    id = Column(Integer, primary_key=True, index=True)
    sample_code = Column(String(100), unique=True, nullable=False, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    sample_type = Column(String(100), nullable=False)
    collection_date = Column(DateTime(timezone=True), nullable=True)
    received_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="Collected")
    storage_location = Column(String(150), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    hospital = relationship("Hospital", back_populates="samples")
    patient = relationship("Patient", back_populates="samples")
    analysis_results = relationship("AnalysisResult", back_populates="sample", cascade="all, delete-orphan")


# ==========================================================
# ANALYSIS RESULTS
# ==========================================================

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    pipeline_version = Column(String(100), default="METHYLOX Analysis v1.0")
    qc_status = Column(String(50), nullable=True)
    metrics = Column(JSON, nullable=True)
    classification = Column(String(150), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    hospital = relationship("Hospital", back_populates="analysis_results")
    sample = relationship("Sample", back_populates="analysis_results")


# ==========================================================
# AUDIT LOG
# ==========================================================

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    action = Column(String(150), nullable=False)
    module = Column(String(100), nullable=False)
    entity = Column(String(150), nullable=True)
    changes = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ------------------------------------------------------
    # ADVANCED AUDIT TRAIL
    # ------------------------------------------------------
    ip_address = Column(String(45), nullable=True)
    endpoint = Column(String(255), nullable=True)
    http_method = Column(String(10), nullable=True)
    status_code = Column(Integer, nullable=True)

    hospital = relationship("Hospital", back_populates="audit_logs")


# ==========================================================
# PERMISSIONS
# ==========================================================

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    module = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_permissions = relationship("UserPermission", back_populates="permission", cascade="all, delete-orphan")


# ==========================================================
# USER PERMISSIONS
# ==========================================================

class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    granted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", foreign_keys=[user_id], back_populates="permissions")
    permission = relationship("Permission", back_populates="user_permissions")
    granted_by_user = relationship("User", foreign_keys=[granted_by])
