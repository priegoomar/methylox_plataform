from datetime import datetime, timezone

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
