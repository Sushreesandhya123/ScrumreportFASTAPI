from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
# from app.modules import IndividualPerformanceCreate, IndividualPerformanceUpdate, IndividualPerformanceResponse
from app.modules.individualperformance import IndividualPerformance
from app.database import get_db
from app.modules.sprint import Sprint
from pydantic import BaseModel
router = APIRouter()


class IndividualPerformanceBase(BaseModel):
    member_name: str
    planned_story_points: int
    completed_story_points: int
    incomplete_story_points: int
class IndividualPerformanceCreate(IndividualPerformanceBase):
    pass
class IndividualPerformanceUpdate(IndividualPerformanceBase):
    pass
class IndividualPerformanceResponse(IndividualPerformanceBase):
    performance_id: int
    sprint_id: int
class Config:
        orm_mode = True    

def get_latest_sprint_id(db: Session) -> int:
    sprint = db.query(Sprint).order_by(Sprint.sprint_id.desc()).first()
    if sprint is None:
        raise HTTPException(status_code=404, detail="No sprints available")
    return sprint.sprint_id

@router.post("/individualperformance/", response_model=IndividualPerformanceResponse)
def create_individual_performance(performance: IndividualPerformanceCreate, db: Session = Depends(get_db)):
    sprint_id = get_latest_sprint_id(db)
    db_performance = IndividualPerformance(**performance.dict(), sprint_id=sprint_id)
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
    sprint_id = get_latest_sprint_id(db)
    for key, value in performance.dict(exclude_unset=True).items():
        setattr(db_performance, key, value)
    db_performance.sprint_id = sprint_id
    
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
