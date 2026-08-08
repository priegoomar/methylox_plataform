from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import TokenData, PermissionGuard


router = APIRouter(prefix="/api/v1/patients", tags=["Patients"])


# ============================================================
# CREATE PATIENT
# ============================================================

@router.post("/", response_model=schemas.PatientResponse)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(PermissionGuard("patient_create"))
):
    existing = db.query(models.Patient).filter(models.Patient.patient_code == patient.patient_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient code already exists")

    new_patient = models.Patient(
        hospital_id=current_user.id_hospital,
        patient_code=patient.patient_code,
        demographics=patient.demographics,
        clinical_notes=patient.clinical_notes,
        created_by=current_user.id_user
    )

    try:
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)

        audit = models.AuditLog(
            user_id=current_user.id_user,
            hospital_id=current_user.id_hospital,
            action="CREATE_PATIENT",
            module="patients",
            entity=new_patient.patient_code,
            changes={"patient_id": new_patient.id, "hospital_id": current_user.id_hospital}
        )
        db.add(audit)
        db.commit()

        return new_patient
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create patient: {str(e)}")


# ============================================================
# GET ALL PATIENTS BY HOSPITAL
# ============================================================

@router.get("/", response_model=list[schemas.PatientResponse])
def get_patients(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(PermissionGuard("patient_read"))
):
    query = db.query(models.Patient)
    if current_user.role != "admin":
        query = query.filter(models.Patient.hospital_id == current_user.id_hospital)
    return query.all()


# ============================================================
# GET PATIENT BY ID
# ============================================================

@router.get("/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(PermissionGuard("patient_read"))
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if current_user.role != "admin" and patient.hospital_id != current_user.id_hospital:
        raise HTTPException(status_code=403, detail="Hospital access denied")

    return patient
