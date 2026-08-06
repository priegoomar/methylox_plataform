from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.security import TokenData, PermissionGuard


router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])


# ============================================================
# GET SAMPLE REPORT
# ============================================================

@router.get("/sample/{sample_id}")
def get_sample_report(
    sample_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(PermissionGuard("report_read"))
):
    sample = db.query(models.Sample).filter(models.Sample.id == sample_id).first()

    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    # ========================================================
    # HOSPITAL ISOLATION
    # ========================================================

    if current_user.role != "admin" and sample.hospital_id != current_user.id_hospital:
        raise HTTPException(status_code=403, detail="Hospital access denied")

    patient = db.query(models.Patient).filter(models.Patient.id == sample.patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    analyses = db.query(models.AnalysisResult).filter(models.AnalysisResult.sample_id == sample_id).all()

    # ========================================================
    # AUDIT LOG
    # ========================================================

    audit = models.AuditLog(
        user_id=current_user.id_user,
        action="VIEW_REPORT",
        module="reports",
        entity=sample.sample_code,
        changes={
            "sample_id": sample.id,
            "sample_code": sample.sample_code,
            "patient_id": patient.id,
            "hospital_id": current_user.id_hospital
        }
    )

    db.add(audit)
    db.commit()

    return {
        "patient": {
            "id": patient.id,
            "patient_code": patient.patient_code,
            "demographics": patient.demographics,
            "clinical_notes": patient.clinical_notes
        },
        "sample": {
            "id": sample.id,
            "sample_code": sample.sample_code,
            "type": sample.sample_type,
            "collection_date": sample.collection_date,
            "received_date": sample.received_date,
            "status": sample.status,
            "storage_location": sample.storage_location
        },
        "analysis_results": [
            {
                "id": result.id,
                "pipeline": result.pipeline_version,
                "qc_status": result.qc_status,
                "metrics": result.metrics,
                "classification": result.classification,
                "created_by": result.created_by,
                "created_at": result.created_at
            }
            for result in analyses
        ],
        "generated_by": {
            "user_id": current_user.id_user,
            "username": current_user.username,
            "role": current_user.role
        }
    }
