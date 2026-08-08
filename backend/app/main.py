from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine, SessionLocal
from app import models
from app.routers import (
    auth,
    patients,
    samples,
    analysis,
    reports,
    access,
    users,
    audit
)

# ==========================================
# APPLICATION CORE
# ==========================================

app = FastAPI(
    title="METHYLOX",
    version="3.0.0",
    description=(
        "METHYLOX molecular intelligence platform "
        "with LIMS, analysis workflows, reporting "
        "and access control."
    )
)

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# HTTP AUDIT TRAIL MIDDLEWARE
# ==========================================

@app.middleware("http")
async def audit_http_requests(request: Request, call_next):
    """
    Global HTTP audit middleware.

    Records:
    - IP address
    - endpoint
    - HTTP method
    - status code
    - timestamp

    Business-level actions such as CREATE_USER,
    CHANGE_PASSWORD, CREATE_PATIENT, etc. continue
    to be recorded by their respective routers.
    """
    skip_paths = {
        "/api/v1/audit/",
        "/api/v1/health",
    }

    should_audit = request.url.path not in skip_paths
    client_ip = request.client.host if request.client else None
    response = None

    try:
        response = await call_next(request)
        return response
    finally:
        if should_audit and response is not None:
            db = SessionLocal()
            try:
                audit_log = models.AuditLog(
                    user_id=None,
                    action="HTTP_REQUEST",
                    module="system",
                    entity=request.url.path,
                    changes={
                        "ip_address": client_ip,
                        "endpoint": request.url.path,
                        "http_method": request.method,
                        "status_code": response.status_code
                    },
                    hospital_id=None,
                    ip_address=client_ip,
                    endpoint=request.url.path,
                    http_method=request.method,
                    status_code=response.status_code
                )
                db.add(audit_log)
                db.commit()
            except Exception:
                db.rollback()
            finally:
                db.close()

# ==========================================
# ROUTERS
# ==========================================

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(samples.router)
app.include_router(analysis.router)
app.include_router(reports.router)
app.include_router(access.router)
app.include_router(users.router)
app.include_router(audit.router)

# ==========================================
# DEBUG DATABASE
# ==========================================

@app.get("/api/v1/debug/database")
def debug_database():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version_num FROM alembic_version"))
        return {"alembic_version": [row[0] for row in result]}

# ==========================================
# DEBUG PATIENT COLUMNS
# ==========================================

@app.get("/api/v1/debug/patients-columns")
def debug_patients_columns():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='patients'
                ORDER BY ordinal_position
            """)
        )
        return {"columns": [row[0] for row in result]}

# ==========================================
# DEBUG SAMPLE COLUMNS
# ==========================================

@app.get("/api/v1/debug/samples-columns")
def debug_samples_columns():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='samples'
                ORDER BY ordinal_position
            """)
        )
        return {"columns": [row[0] for row in result]}

# ==========================================
# CREATE DEFAULT HOSPITAL
# ==========================================

@app.get("/api/v1/debug/create-default-hospital")
def create_default_hospital():
    db = SessionLocal()
    try:
        hospital = db.query(models.Hospital).filter(models.Hospital.id == 1).first()
        if hospital:
            return {"status": "already exists", "id": hospital.id}

        hospital = models.Hospital(id=1, name="Hospital Universitario")
        db.add(hospital)
        db.commit()
        return {"status": "created", "id": 1}
    finally:
        db.close()

# ==========================================
# TEMP FIX USERS HOSPITAL
# ==========================================

@app.get("/api/v1/debug/fix-users-hospital")
def fix_users_hospital():
    db = SessionLocal()
    try:
        updated = (
            db.query(models.User)
            .filter(models.User.hospital_id == None)
            .update({models.User.hospital_id: 1})
        )
        db.commit()
        return {"status": "updated", "users_updated": updated}
    finally:
        db.close()

# ==========================================
# TEMP FIX PATIENTS HOSPITAL
# ==========================================

@app.get("/api/v1/debug/fix-patients-hospital")
def fix_patients_hospital():
    db = SessionLocal()
    try:
        updated = (
            db.query(models.Patient)
            .filter(models.Patient.hospital_id == None)
            .update({models.Patient.hospital_id: 1})
        )
        db.commit()
        return {"status": "updated", "patients_updated": updated}
    finally:
        db.close()

# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/api/v1/health", tags=["System"])
def health():
    return {
        "status": "ONLINE",
        "system": "METHYLOX",
        "version": "3.0.0",
        "timestamp": datetime.now(timezone.utc)
    }

# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():
    return {
        "system": "METHYLOX",
        "status": "running",
        "version": "3.0.0"
    }
