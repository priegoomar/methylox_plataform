from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import (get_current_user_claims, TokenData, PermissionGuard)


router = APIRouter(
    prefix="/api/v1/patients",
    tags=["Patients"]
)


# ==========================================
# CREATE PATIENT
# ==========================================

@router.post(
    "/",
    response_model=schemas.PatientResponse
)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(
        PermissionGuard("patient_create")
    )
):
    existing = (
        db.query(models.Patient)
        .filter(
            models.Patient.patient_code == patient.patient_code
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Patient code already exists"
        )

    new_patient = models.Patient(
        patient_code=patient.patient_code,
        demographics=patient.demographics,
        clinical_notes=patient.clinical_notes,
        created_by=current_user.id_user
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


# ==========================================
# GET ALL PATIENTS
# ==========================================

@router.get(
    "/",
    response_model=list[schemas.PatientResponse]
)
def get_patients(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(
        PermissionGuard("patient_read")
    )
):
    patients = (
        db.query(models.Patient)
        .all()
    )

    return patients


# ==========================================
# GET PATIENT BY ID
# ==========================================

@router.get(
    "/{patient_id}",
    response_model=schemas.PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(
        PermissionGuard("patient_read")
    )
):
    patient = (
        db.query(models.Patient)
        .filter(
            models.Patient.id == patient_id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient
