from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.production_pipeline_releases import ProductionPipelineRelease 
from typing import List
from pydantic import BaseModel
from app.modules.sprint import Sprint


router = APIRouter()

class ProductionPipelineReleaseBase(BaseModel):
    app_name: str
    release_number: str
class ProductionPipelineReleaseCreate(ProductionPipelineReleaseBase):
    pass
class ProductionPipelineReleaseUpdate(ProductionPipelineReleaseBase):
    pass
class ProductionPipelineReleaseResponse(ProductionPipelineReleaseBase):
    release_id: int
    sprint_id: int
    
class Config:
        orm_mode = True



def get_latest_sprint_id(db: Session) -> int:
    sprint = db.query(Sprint).order_by(Sprint.sprint_id.desc()).first()
    if sprint is None:
        raise HTTPException(status_code=404, detail="No sprints available")
    return sprint.sprint_id

@router.post("/production_pipeline_releases/", response_model=ProductionPipelineReleaseResponse)
def create_production_pipeline_release(release: ProductionPipelineReleaseCreate, db: Session = Depends(get_db)):
    sprint_id = get_latest_sprint_id(db)
    db_release = ProductionPipelineRelease(**release.dict(), sprint_id=sprint_id)
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
    sprint_id = get_latest_sprint_id(db)
    for key, value in release.dict().items():
        setattr(db_release, key, value)
    db_release.sprint_id = sprint_id    
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
