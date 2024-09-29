from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.modules.schemas import IndividualPerformanceCreate, IndividualPerformanceUpdate, IndividualPerformanceResponse
from app.modules.individualperformance import IndividualPerformance
from app.database import get_db
from app.modules.sprint import Sprint
router = APIRouter()

@router.post("/individualperformance/", response_model=IndividualPerformanceResponse)
def create_individual_performance(performance: IndividualPerformanceCreate, db: Session = Depends(get_db)):
    # Check if sprint_id exists in sprints table
    sprint = db.query(Sprint).filter(Sprint.sprint_id == performance.sprint_id).first()
    if sprint is None:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    # Create and save the new individual performance record
    db_performance = IndividualPerformance(**performance.dict())
    db.add(db_performance)
    db.commit()
    db.refresh(db_performance)
    return db_performance

@router.get("/individualperformance/", response_model=List[IndividualPerformanceResponse])
def read_individual_performances(db: Session = Depends(get_db)):
    return db.query(IndividualPerformance).all()

@router.get("/individualperformance/{performance_id}", response_model=IndividualPerformanceResponse)
def read_individual_performance(performance_id: int, db: Session = Depends(get_db)):
    db_performance = db.query(IndividualPerformance).filter(IndividualPerformance.performance_id == performance_id).first()
    if db_performance is None:
        raise HTTPException(status_code=404, detail="IndividualPerformance not found")
    return db_performance

@router.put("/individualperformance/{performance_id}", response_model=IndividualPerformanceResponse)
def update_individual_performance(performance_id: int, performance: IndividualPerformanceUpdate, db: Session = Depends(get_db)):
    db_performance = db.query(IndividualPerformance).filter(IndividualPerformance.performance_id == performance_id).first()
    if db_performance is None:
        raise HTTPException(status_code=404, detail="IndividualPerformance not found")
    if performance.sprint_id:
        sprint = db.query(Sprint).filter(Sprint.sprint_id == performance.sprint_id).first()
        if not sprint:
            raise HTTPException(status_code=404, detail="Sprint not found")
    for key, value in performance.dict(exclude_unset=True).items():
        setattr(db_performance, key, value)
    
    db.commit()
    db.refresh(db_performance)
    return db_performance

@router.delete("/individualperformance/{performance_id}")
def delete_individual_performance(performance_id: int, db: Session = Depends(get_db)):
    db_performance = db.query(IndividualPerformance).filter(IndividualPerformance.performance_id == performance_id).first()
    if db_performance is None:
        raise HTTPException(status_code=404, detail="IndividualPerformance not found")
    db.delete(db_performance)
    db.commit()
    return {"detail": "IndividualPerformance deleted"}
