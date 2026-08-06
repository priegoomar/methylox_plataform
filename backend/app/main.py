from datetime import datetime, timezone
from sqlalchemy import text
from app.database import engine

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/api/v1/debug/database")
def debug_database():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT version_num 
            FROM alembic_version
        """))

        return {
            "alembic_version": [row[0] for row in result]
        }


@app.get("/api/v1/debug/patients-columns")
def debug_columns():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='patients'
        """))

        return {
            "columns": [row[0] for row in result]
        }

@app.get("/api/v1/debug/fix-hospital")
def fix_hospital():

    with engine.connect() as conn:

        conn.execute(text("""
            ALTER TABLE patients
            ADD COLUMN IF NOT EXISTS hospital_id INTEGER;
        """))

        conn.execute(text("""
            UPDATE patients
            SET hospital_id = 1
            WHERE hospital_id IS NULL;
        """))

        conn.commit()

    return {
        "status": "OK",
        "message": "hospital_id column fixed"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get(
    "/api/v1/health",
    tags=["System"]
)
def health():
    return {
        "status": "ONLINE",
        "system": "METHYLOX",
        "version": "3.0.0",
        "timestamp": datetime.now(timezone.utc)
    }
