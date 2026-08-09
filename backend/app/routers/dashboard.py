from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models
from app.security import TokenData, PermissionGuard


router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(PermissionGuard("dashboard_read"))
):
    """
    Returns real-time dashboard metrics.

    Non-admin users:
        Only see data belonging to their hospital.

    Admin users:
        Can see system-wide data.
    """
    patients_query = db.query(models.Patient)
    samples_query = db.query(models.Sample)
    analysis_query = db.query(models.AnalysisResult)

    if current_user.role != "admin":
        patients_query = patients_query.filter(models.Patient.hospital_id == current_user.id_hospital)
        samples_query = samples_query.filter(models.Sample.hospital_id == current_user.id_hospital)
        analysis_query = analysis_query.filter(models.AnalysisResult.hospital_id == current_user.id_hospital)

    total_patients = patients_query.count()
    total_samples = samples_query.count()
    samples_received_today = samples_query.filter(func.date(models.Sample.received_date) == func.current_date()).count()
    active_workflow = samples_query.filter(models.Sample.status.in_(["Collected", "Received", "Processing", "In Analysis"])).count()
    ready_reports = analysis_query.filter(models.AnalysisResult.qc_status == "PASS").count()
    total_analysis = analysis_query.count()

    classification_rows = analysis_query.with_entities(models.AnalysisResult.classification, func.count(models.AnalysisResult.id)).group_by(models.AnalysisResult.classification).all()
    classifications = {c or "Unknown": count for c, count in classification_rows}

    status_rows = samples_query.with_entities(models.Sample.status, func.count(models.Sample.id)).group_by(models.Sample.status).all()
    sample_status = {s or "Unknown": count for s, count in status_rows}

    return {
        "hospital_id": current_user.id_hospital,
        "metrics": {
            "total_patients": total_patients,
            "total_samples": total_samples,
            "samples_received_today": samples_received_today,
            "active_workflow": active_workflow,
            "ready_reports": ready_reports,
            "total_analysis": total_analysis
        },
        "classifications": classifications,
        "sample_status": sample_status
    }
