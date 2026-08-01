from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/api/v1/samples",
    tags=["Samples"]
)


# ==========================================
# CREATE SAMPLE
# ==========================================

@router.post("/", response_model=schemas.SampleResponse)
def create_sample(
    sample: schemas.SampleCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(models.Sample)
        .filter(models.Sample.sample_code == sample.sample_code)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Sample code already exists"
        )

    patient = (
        db.query(models.Patient)
        .filter(models.Patient.id == sample.patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    new_sample = models.Sample(
        sample_code=sample.sample_code,
        patient_id=sample.patient_id,
        sample_type=sample.sample_type,
        collection_date=sample.collection_date,
        received_date=sample.received_date,
        status=sample.status,
        storage_location=sample.storage_location
    )

    db.add(new_sample)
    db.commit()
    db.refresh(new_sample)

    return new_sample


# ==========================================
# GET SAMPLES
# ==========================================

@router.get("/", response_model=list[schemas.SampleResponse])
def get_samples(
    status: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Sample)

    if status:
        query = query.filter(models.Sample.status == status)

    return query.all()


# ==========================================
# GET SAMPLE BY ID
# ==========================================

@router.get("/{sample_id}", response_model=schemas.SampleResponse)
def get_sample(
    sample_id: int,
    db: Session = Depends(get_db)
):
    sample = (
        db.query(models.Sample)
        .filter(models.Sample.id == sample_id)
        .first()
    )

    if not sample:
        raise HTTPException(
            status_code=404,
            detail="Sample not found"
        )

    return sample


# ==========================================
# UPDATE SAMPLE STATUS
# ==========================================

@router.patch("/{sample_id}", response_model=schemas.SampleResponse)
def update_sample(
    sample_id: int,
    update: schemas.SampleUpdate,
    db: Session = Depends(get_db)
):
    sample = (
        db.query(models.Sample)
        .filter(models.Sample.id == sample_id)
        .first()
    )

    if not sample:
        raise HTTPException(
            status_code=404,
            detail="Sample not found"
        )

    if update.status:
        sample.status = update.status

    if update.storage_location:
        sample.storage_location = update.storage_location

    if update.received_date:
        sample.received_date = update.received_date

    sample.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(sample)
    return sample
