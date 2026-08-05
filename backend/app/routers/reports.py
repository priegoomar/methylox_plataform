from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.security import TokenData, PermissionGuard

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])


@router.get("/sample/{sample_id}")
def get_sample_report(
    sample_id: int,
    db: Session = Depends(get_db),
    # CORRECCIÓN: antes usaba get_current_user_claims (solo exige estar
    # logueado, sin importar rol/permiso). Todo el resto del backend
    # (samples, patients, analysis) protege por permiso específico con
    # PermissionGuard. Este reporte incluye demographics completos y notas
    # clínicas del paciente, así que amerita el mismo nivel de control.
    # NOTA: requiere que exista el permiso "report_read" sembrado en la
    # tabla permissions y asignado a los roles/usuarios correspondientes.
    current_user: TokenData = Depends(PermissionGuard("report_read")),
):
    sample = db.query(models.Sample).filter(models.Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    patient = db.query(models.Patient).filter(models.Patient.id == sample.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    analyses = db.query(models.AnalysisResult).filter(models.AnalysisResult.sample_id == sample_id).all()

    # NOTA: este log se sigue escribiendo en cada GET (cada vista previa),
    # no solo cuando se descarga el PDF final. Si el registro de auditoría
    # debe reflejar solo descargas reales, conviene mover este audit log a
    # un endpoint separado que el frontend llame únicamente al confirmar
    # la descarga (por ejemplo POST /reports/sample/{id}/download-event).
    audit = models.AuditLog(
        user_id=current_user.id_user,
        action="GENERATE_REPORT",
        module="reports",
        entity=sample.sample_code,
        changes={"sample_id": sample.id, "sample_code": sample.sample_code, "patient_id": patient.id},
    )
    db.add(audit)
    db.commit()

    return {
        "patient": {
            "id": patient.id,
            "patient_code": patient.patient_code,
            "demographics": patient.demographics,
            "clinical_notes": patient.clinical_notes,
        },
        "sample": {
            "id": sample.id,
            "sample_code": sample.sample_code,
            "type": sample.sample_type,
            "collection_date": sample.collection_date,
            "received_date": sample.received_date,
            "status": sample.status,
            "storage_location": sample.storage_location,
        },
        "analysis_results": [
            {
                "id": result.id,
                "pipeline": result.pipeline_version,
                "qc_status": result.qc_status,
                "metrics": result.metrics,
                "classification": result.classification,
                "created_by": result.created_by,
                "created_at": result.created_at,
            }
            for result in analyses
        ],
        "generated_by": {
            "user_id": current_user.id_user,
            "username": current_user.username,
            "role": current_user.role,
        },
    }
