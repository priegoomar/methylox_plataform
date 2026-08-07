from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import (
    TokenData,
    PermissionGuard
)


router = APIRouter(
    prefix="/api/v1/samples",
    tags=["Samples"]
)


# ============================================================
# CREATE SAMPLE
# ============================================================

@router.post("/", response_model=schemas.SampleResponse)
def create_sample(
    sample: schemas.SampleCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(PermissionGuard("sample_create"))
):
    existing = db.query(models.Sample).filter(models.Sample.sample_code == sample.sample_code).first()

    if existing:
        raise HTTPException(status_code=400, detail="Sample code already exists")

    patient = db.query(models.Patient).filter(models.Patient.id == sample.patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if current_user.role != "admin" and patient.hospital_id != current_user.id_hospital:
        raise HTTPException(status_code=403, detail="Patient belongs to another hospital")

    new_sample = models.Sample(
        hospital_id=patient.hospital_id,
        sample_code=sample.sample_code,
        patient_id=sample.patient_id,
        sample_type=sample.sample_type,
        collection_date=sample.collection_date,
        received_date=sample.received_date,
        status=sample.status,
        storage_location=sample.storage_location,
        created_by=current_user.id_user
    )

    db.add(new_sample)
    db.commit()
    db.refresh(new_sample)

    audit = models.AuditLog(
        user_id=current_user.id_user,
        action="CREATE_SAMPLE",
        module="samples",
        entity=new_sample.sample_code,
        changes={
            "sample_id": new_sample.id,
            "hospital_id": current_user.id_hospital
        }
    )

    db.add(audit)
    db.commit()

    return new_sample


# ============================================================
# GET SAMPLES WITH HOSPITAL FILTER
# ============================================================

@router.get("/", response_model=list[schemas.SampleResponse])
def get_samples(
    status: str | None = None,
    patient_id: int | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(PermissionGuard("sample_read"))
):
    query = db.query(models.Sample)

    if current_user.role != "admin":
        query = query.filter(models.Sample.hospital_id == current_user.id_hospital)

    if status:
        query = query.filter(models.Sample.status == status)

    if patient_id:
        query = query.filter(models.Sample.patient_id == patient_id)

    if start_date:
        query = query.filter(models.Sample.collection_date >= start_date)

    if end_date:
        query = query.filter(models.Sample.collection_date <= end_date)

    return query.all()


# ============================================================
# GET SAMPLE BY ID
# ============================================================

@router.get("/{sample_id}", response_model=schemas.SampleResponse)
def get_sample(
    sample_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(PermissionGuard("sample_read"))
):
    sample = db.query(models.Sample).filter(models.Sample.id == sample_id).first()

    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    if current_user.role != "admin" and sample.hospital_id != current_user.id_hospital:
        raise HTTPException(status_code=403, detail="Hospital access denied")

    return sample


# ============================================================
# UPDATE SAMPLE
# ============================================================

@router.patch("/{sample_id}", response_model=schemas.SampleResponse)
def update_sample(
    sample_id: int,
    update: schemas.SampleUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(PermissionGuard("sample_update"))
):
    sample = db.query(models.Sample).filter(models.Sample.id == sample_id).first()

    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    if current_user.role != "admin" and sample.hospital_id != current_user.id_hospital:
        raise HTTPException(status_code=403, detail="Hospital access denied")

    if update.status:
        sample.status = update.status

    if update.storage_location:
        sample.storage_location = update.storage_location

    if update.received_date:
        sample.received_date = update.received_date

    sample.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(sample)

    return sample
