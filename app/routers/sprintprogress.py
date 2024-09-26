from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.modules.schemas import SprintProgressCreate, SprintProgressUpdate, SprintProgressResponse  # Import Pydantic models
from app.modules.sprintprogress import SprintProgress  # Import SQLAlchemy model
from app.database import get_db

router = APIRouter()

@router.post("/sprintprogress/", response_model=SprintProgressResponse)
def create_sprintprogress(sprintprogress: SprintProgressCreate, db: Session = Depends(get_db)):
    db_sprintprogress = SprintProgress(**sprintprogress.dict())
    db.add(db_sprintprogress)
    db.commit()
    db.refresh(db_sprintprogress)
    return db_sprintprogress

@router.get("/sprintprogress/", response_model=List[SprintProgressResponse])
def read_sprintprogress(db: Session = Depends(get_db)):
    return db.query(SprintProgress).all()

@router.get("/sprintprogress/{progress_id}", response_model=SprintProgressResponse)
def read_sprintprogress(progress_id: int, db: Session = Depends(get_db)):
    db_sprintprogress = db.query(SprintProgress).filter(SprintProgress.progress_id == progress_id).first()
    if db_sprintprogress is None:
        raise HTTPException(status_code=404, detail="SprintProgress not found")
    return db_sprintprogress

@router.put("/sprintprogress/{progress_id}", response_model=SprintProgressResponse)
def update_sprintprogress(progress_id: int, sprintprogress: SprintProgressUpdate, db: Session = Depends(get_db)):
    db_sprintprogress = db.query(SprintProgress).filter(SprintProgress.progress_id == progress_id).first()
    if db_sprintprogress is None:
        raise HTTPException(status_code=404, detail="SprintProgress not found")
    for key, value in sprintprogress.dict().items():
        setattr(db_sprintprogress, key, value)
    db.commit()
    db.refresh(db_sprintprogress)
    return db_sprintprogress

@router.delete("/sprintprogress/{progress_id}")
def delete_sprintprogress(progress_id: int, db: Session = Depends(get_db)):
    db_sprintprogress = db.query(SprintProgress).filter(SprintProgress.progress_id == progress_id).first()
    if db_sprintprogress is None:
        raise HTTPException(status_code=404, detail="SprintProgress not found")
    db.delete(db_sprintprogress)
    db.commit()
    return {"detail": "SprintProgress deleted"}
