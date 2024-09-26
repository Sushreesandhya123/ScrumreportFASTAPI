from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.sprint import Sprint
from app.modules.team import Team  # Importing Team to validate team_id
from app.database import SessionLocal
from datetime import date

router = APIRouter()


class SprintBase(BaseModel):
    team_id: int
    sprint_number: int
    sprint_duration: str
    date_of_report: date = Field(..., description="Date of the report in YYYY-MM-DD format")
    scrum_master: str

class SprintCreate(SprintBase):
    pass

class SprintUpdate(SprintBase):
    pass

class SprintResponse(SprintBase):
    sprint_id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sprints/", response_model=SprintResponse)
def create_sprint(sprint: SprintCreate, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.team_id == sprint.team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    db_sprint = Sprint(**sprint.dict())
    db.add(db_sprint)
    db.commit()
    db.refresh(db_sprint)
    return db_sprint

@router.get("/sprints/", response_model=List[SprintResponse])
def read_sprints(db: Session = Depends(get_db)):
    return db.query(Sprint).all()

@router.get("/sprints/{sprint_id}", response_model=SprintResponse)
def read_sprint(sprint_id: int, db: Session = Depends(get_db)):
    sprint = db.query(Sprint).filter(Sprint.sprint_id == sprint_id).first()
    if sprint is None:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint

@router.put("/sprints/{sprint_id}", response_model=SprintResponse)
def update_sprint(sprint_id: int, sprint: SprintUpdate, db: Session = Depends(get_db)):
    db_sprint = db.query(Sprint).filter(Sprint.sprint_id == sprint_id).first()
    if db_sprint is None:
        raise HTTPException(status_code=404, detail="Sprint not found")
    team = db.query(Team).filter(Team.team_id == sprint.team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    for key, value in sprint.dict().items():
        setattr(db_sprint, key, value)
    db.commit()
    db.refresh(db_sprint)
    return db_sprint

@router.delete("/sprints/{sprint_id}")
def delete_sprint(sprint_id: int, db: Session = Depends(get_db)):
    db_sprint = db.query(Sprint).filter(Sprint.sprint_id == sprint_id).first()
    if db_sprint is None:
        raise HTTPException(status_code=404, detail="Sprint not found")
    db.delete(db_sprint)
    db.commit()
    return {"detail": "Sprint deleted"}
