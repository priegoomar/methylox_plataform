from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import (get_current_user_claims, TokenData, PermissionGuard)


router = APIRouter(
    prefix="/api/v1/analysis",
    tags=["Analysis"]
)


# ==========================================
# CREATE ANALYSIS RESULT
# ==========================================

@router.post(
    "/",
    response_model=schemas.AnalysisResponse
)
def create_analysis(
    analysis: schemas.AnalysisCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user_claims)
):
    sample = (
        db.query(models.Sample)
        .filter(
            models.Sample.id == analysis.sample_id
        )
        .first()
    )

    if not sample:
        raise HTTPException(
            status_code=404,
            detail="Sample not found"
        )

    new_analysis = models.AnalysisResult(
        sample_id=analysis.sample_id,
        pipeline_version=analysis.pipeline_version,
        qc_status=analysis.qc_status,
        metrics=analysis.metrics,
        classification=analysis.classification,
        created_by=current_user.id_user
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return new_analysis


# ==========================================
# GET ANALYSIS BY SAMPLE
# ==========================================

@router.get(
    "/sample/{sample_id}",
    response_model=list[schemas.AnalysisResponse]
)
def get_sample_analysis(
    sample_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user_claims)
):
    results = (
        db.query(models.AnalysisResult)
        .filter(
            models.AnalysisResult.sample_id == sample_id
        )
        .all()
    )

    return results
