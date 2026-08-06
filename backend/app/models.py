from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="hospital")
    patients = relationship("Patient", back_populates="hospital")
    samples = relationship("Sample", back_populates="hospital")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=True)
    role = Column(String(50), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    hospital = relationship("Hospital", back_populates="users")
    permissions = relationship("UserPermission", foreign_keys="UserPermission.user_id", back_populates="user", cascade="all, delete-orphan")
    direct_permissions = relationship("Permission", secondary="user_permissions", primaryjoin="User.id==UserPermission.user_id", secondaryjoin="Permission.id==UserPermission.permission_id", viewonly=True)

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    patient_code = Column(String(100), unique=True, nullable=False, index=True)
    demographics = Column(JSON, nullable=True)
    clinical_notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    hospital = relationship("Hospital", back_populates="patients")
    samples = relationship("Sample", back_populates="patient", cascade="all, delete-orphan")

class Sample(Base):
    __tablename__ = "samples"
    id = Column(Integer, primary_key=True, index=True)
    sample_code = Column(String(100), unique=True, nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    sample_type = Column(String(100), nullable=False)
    collection_date = Column(DateTime(timezone=True), nullable=True)
    received_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="Collected")
    storage_location = Column(String(150), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    hospital = relationship("Hospital", back_populates="samples")
    patient = relationship("Patient", back_populates="samples")
    analysis_results = relationship("AnalysisResult", back_populates="sample", cascade="all, delete-orphan")
    movements = relationship("SampleMovement", back_populates="sample", cascade="all, delete-orphan", order_by="SampleMovement.created_at")

class SampleMovement(Base):
    __tablename__ = "sample_movements"
    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False, index=True)
    previous_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    notes = Column(String(255), nullable=True)
    performed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sample = relationship("Sample", back_populates="movements")

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    pipeline_version = Column(String(100), default="METHYLOX Analysis v1.0")
    qc_status = Column(String(50), nullable=True)
    metrics = Column(JSON, nullable=True)
    classification = Column(String(150), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sample = relationship("Sample", back_populates="analysis_results")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(150), nullable=False)
    module = Column(String(100), nullable=False)
    entity = Column(String(150), nullable=True)
    changes = Column(JSON, nullable=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    module = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_permissions = relationship("UserPermission", back_populates="permission", cascade="all, delete-orphan")

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
