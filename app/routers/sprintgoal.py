from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from app.modules.sprintgoal import Sprintgoal
from app.database import get_db
from app.modules.sprint import Sprint
from enum import Enum

# Initialize router
router = APIRouter()

class StatusEnum(str, Enum):
    DONE = "Done"
    BACKLOG = "Backlog"
    PENDING = "Pending"

class SprintgoalBase(BaseModel):
    description: str
    status: StatusEnum

class SprintgoalCreate(SprintgoalBase):
    pass

class SprintgoalUpdate(SprintgoalBase):
    pass

class SprintgoalResponse(SprintgoalBase):
    id: int
    sprint_id: int  # Include sprint_id in response

class Config:
        orm_mode = True

def get_latest_sprint_id(db: Session) -> int:
    sprint = db.query(Sprint).order_by(Sprint.sprint_id.desc()).first()
    if sprint is None:
        raise HTTPException(status_code=404, detail="No sprints available")
    return sprint.sprint_id

@router.post("/sprintgoals/", response_model=SprintgoalResponse)
def create_sprintgoal(sprintgoal: SprintgoalCreate, db: Session = Depends(get_db)):
    sprint_id = get_latest_sprint_id(db)
    
    db_sprintgoal = Sprintgoal(**sprintgoal.dict(), sprint_id=sprint_id) 
    db.add(db_sprintgoal)
    db.commit()
    db.refresh(db_sprintgoal)
    return db_sprintgoal

# Read all sprint goals
@router.get("/sprintgoals/", response_model=List[SprintgoalResponse])
def read_sprintgoals(db: Session = Depends(get_db)):
    return db.query(Sprintgoal).all()

# Read a specific sprint goal by ID
@router.get("/sprintgoals/{sprintgoal_id}", response_model=SprintgoalResponse)
def read_sprintgoal(sprintgoal_id: int, db: Session = Depends(get_db)):
    db_sprintgoal = db.query(Sprintgoal).filter(Sprintgoal.id == sprintgoal_id).first()
    if db_sprintgoal is None:
        raise HTTPException(status_code=404, detail="Sprintgoal not found")
    return db_sprintgoal

@router.put("/sprintgoals/{sprintgoal_id}", response_model=SprintgoalResponse)
def update_sprintgoal(sprintgoal_id: int, sprintgoal: SprintgoalUpdate, db: Session = Depends(get_db)):
    db_sprintgoal = db.query(Sprintgoal).filter(Sprintgoal.id == sprintgoal_id).first()
    if db_sprintgoal is None:
        raise HTTPException(status_code=404, detail="Sprintgoal not found")
    sprint_id = get_latest_sprint_id(db)
    for key, value in sprintgoal.dict().items():
        setattr(db_sprintgoal, key, value)
    db_sprintgoal.sprint_id = sprint_id 
    db.commit()
    db.refresh(db_sprintgoal)
    return db_sprintgoal

# Delete a sprint goal
@router.delete("/sprintgoals/{sprintgoal_id}")
def delete_sprintgoal(sprintgoal_id: int, db: Session = Depends(get_db)):
    db_sprintgoal = db.query(Sprintgoal).filter(Sprintgoal.id == sprintgoal_id).first()
    if db_sprintgoal is None:
        raise HTTPException(status_code=404, detail="Sprintgoal not found")
    db.delete(db_sprintgoal)
    db.commit()
    return {"detail": "Sprintgoal deleted"}