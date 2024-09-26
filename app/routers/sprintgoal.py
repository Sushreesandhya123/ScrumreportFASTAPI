from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from app.modules.sprintgoal import Sprintgoal
from app.database import get_db

# Initialize router
router = APIRouter()

class SprintgoalBase(BaseModel):
    description: str
    status: str
    sprint_id: int  

class SprintgoalCreate(SprintgoalBase):
    pass

class SprintgoalUpdate(SprintgoalBase):
    pass

class SprintgoalResponse(SprintgoalBase):
    id: int

    class Config:
        orm_mode = True


@router.post("/sprintgoals/", response_model=SprintgoalResponse)
def create_sprintgoal(sprintgoal: SprintgoalCreate, db: Session = Depends(get_db)):
    db_sprintgoal = Sprintgoal(**sprintgoal.dict())  # Make sure sprint_id is included
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

# Update an existing sprint goal
@router.put("/sprintgoals/{sprintgoal_id}", response_model=SprintgoalResponse)
def update_sprintgoal(sprintgoal_id: int, sprintgoal: SprintgoalUpdate, db: Session = Depends(get_db)):
    db_sprintgoal = db.query(Sprintgoal).filter(Sprintgoal.id == sprintgoal_id).first()
    if db_sprintgoal is None:
        raise HTTPException(status_code=404, detail="Sprintgoal not found")
    for key, value in sprintgoal.dict().items():
        setattr(db_sprintgoal, key, value)
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