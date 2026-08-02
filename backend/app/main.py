from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.routers import auth
from app.routers import patients
from app.routers import samples
from app.routers import analysis
from app.routers import reports
from app.routers import access
from app.routers import users
from app.routers import audit


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

Base.metadata.create_all(bind=engine)


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
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(audit.router, prefix="/api/v1/audit", tags=["Audit Trail"])


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
