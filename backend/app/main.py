from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routers import auth, patients, samples, analysis, reports, access, users, audit, hospitals

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="METHYLOX",
    version="3.0.0",
    description="METHYLOX molecular intelligence platform with LIMS, analysis workflows, reporting and access control."
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(samples.router)
app.include_router(analysis.router)
app.include_router(reports.router)
app.include_router(access.router)
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(audit.router, prefix="/api/v1/audit", tags=["Audit Trail"])
app.include_router(hospitals.router)

@app.get("/api/v1/health", tags=["System"])
def health():
    return {"status": "ONLINE", "system": "METHYLOX", "version": "3.0.0", "timestamp": datetime.now(timezone.utc)}
