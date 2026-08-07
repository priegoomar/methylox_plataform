from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/api/v1/debug/patients-columns")
def debug_patients_columns():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT column_name FROM information_schema.columns WHERE table_name='patients' ORDER BY ordinal_position")
        )
        return {"columns": [row[0] for row in result]}


@app.get("/api/v1/debug/samples-columns")
def debug_samples_columns():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT column_name FROM information_schema.columns WHERE table_name='samples' ORDER BY ordinal_position")
        )
        return {"columns": [row[0] for row in result]}


# ==========================================
# TEMP FIX USERS HOSPITAL
# ==========================================
@app.get("/api/v1/debug/fix-users-hospital")
def fix_users_hospital():
    from app.database import SessionLocal
    from app import models

    db = SessionLocal()
    updated = db.query(models.User).filter(models.User.hospital_id == None).update({models.User.hospital_id: 1})
    db.commit()
    db.close()
    return {"status": "updated", "users_updated": updated}


# ==========================================
# TEMP FIX ADMIN HOSPITAL
# ==========================================
@app.get("/api/v1/debug/fix-admin-hospital")
def fix_admin_hospital():
    from app.database import SessionLocal
    from app import models

    db = SessionLocal()
    admin = db.query(models.User).filter(models.User.username == "admin@methylox.com").first()
    if not admin:
        db.close()
        return {"error": "Admin not found"}

    admin.hospital_id = 1
    db.commit()
    db.refresh(admin)
    db.close()
    return {"status": "updated", "username": admin.username, "hospital_id": admin.hospital_id}


# ==========================================
# TEMP FIX PATIENTS HOSPITAL
# ==========================================
@app.get("/api/v1/debug/fix-patients-hospital")
def fix_patients_hospital():
    from app.database import SessionLocal
    from app import models

    db = SessionLocal()
    updated = db.query(models.Patient).filter(models.Patient.hospital_id == None).update({models.Patient.hospital_id: 1})
    db.commit()
    db.close()
    return {"status": "updated", "patients_updated": updated}


# ==========================================
# HEALTH CHECK & ROOT
# ==========================================
@app.get("/api/v1/health", tags=["System"])
def health():
    return {
        "status": "ONLINE",
        "system": "METHYLOX",
        "version": "3.0.0",
        "timestamp": datetime.now(timezone.utc)
    }


@app.get("/")
def root():
    return {
        "system": "METHYLOX",
        "status": "running",
        "version": "3.0.0"
    }
