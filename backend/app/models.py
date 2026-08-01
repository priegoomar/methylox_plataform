from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


# ==========================================
# USER MODEL
# ==========================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=True)
    role = Column(String(50), default="viewer")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)


# ==========================================
# PATIENT MODEL
# ==========================================

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_code = Column(String(100), unique=True, nullable=False, index=True)
    demographics = Column(JSON, nullable=True)
    clinical_notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    samples = relationship("Sample", back_populates="patient")


# ==========================================
# SAMPLE / LIMS MODEL
# ==========================================

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
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    patient = relationship("Patient", back_populates="samples")
    analysis_results = relationship("AnalysisResult", back_populates="sample")


# ==========================================
# ANALYSIS RESULT MODEL
# ==========================================

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    pipeline_version = Column(String(100), default="METHYLOX Engine v1.0")
    qc_status = Column(String(50), nullable=True)
    metrics = Column(JSON, nullable=True)
    classification = Column(String(150), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sample = relationship("Sample", back_populates="analysis_results")


# ==========================================
# AUDIT LOG MODEL
# ==========================================

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(150), nullable=False)
    module = Column(String(100), nullable=False)
    entity = Column(String(100), nullable=True)
    changes = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
