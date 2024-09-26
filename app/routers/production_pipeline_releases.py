from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.production_pipeline_releases import ProductionPipelineRelease  # Import the model
from app.modules.schemas import ProductionPipelineReleaseCreate, ProductionPipelineReleaseUpdate, ProductionPipelineReleaseResponse
from typing import List

router = APIRouter()

@router.post("/production_pipeline_releases/", response_model=ProductionPipelineReleaseResponse)
def create_production_pipeline_release(release: ProductionPipelineReleaseCreate, db: Session = Depends(get_db)):
    db_release = ProductionPipelineRelease(**release.dict())
    db.add(db_release)
    db.commit()
    db.refresh(db_release)
    return db_release

@router.get("/production_pipeline_releases/", response_model=List[ProductionPipelineReleaseResponse])
def read_production_pipeline_releases(db: Session = Depends(get_db)):
    return db.query(ProductionPipelineRelease).all()

@router.get("/production_pipeline_releases/{release_id}", response_model=ProductionPipelineReleaseResponse)
def read_production_pipeline_release(release_id: int, db: Session = Depends(get_db)):
    db_release = db.query(ProductionPipelineRelease).filter(ProductionPipelineRelease.release_id == release_id).first()
    if db_release is None:
        raise HTTPException(status_code=404, detail="Production Pipeline Release not found")
    return db_release

@router.put("/production_pipeline_releases/{release_id}", response_model=ProductionPipelineReleaseResponse)
def update_production_pipeline_release(release_id: int, release: ProductionPipelineReleaseUpdate, db: Session = Depends(get_db)):
    db_release = db.query(ProductionPipelineRelease).filter(ProductionPipelineRelease.release_id == release_id).first()
    if db_release is None:
        raise HTTPException(status_code=404, detail="Production Pipeline Release not found")
    for key, value in release.dict().items():
        setattr(db_release, key, value)
    db.commit()
    db.refresh(db_release)
    return db_release

@router.delete("/production_pipeline_releases/{release_id}")
def delete_production_pipeline_release(release_id: int, db: Session = Depends(get_db)):
    db_release = db.query(ProductionPipelineRelease).filter(ProductionPipelineRelease.release_id == release_id).first()
    if db_release is None:
        raise HTTPException(status_code=404, detail="Production Pipeline Release not found")
    db.delete(db_release)
    db.commit()
    return {"detail": "Production Pipeline Release deleted"}
