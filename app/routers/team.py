from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from app.modules.team import Team
from app.database import SessionLocal

# Initialize the router
router = APIRouter()

class TeamBase(BaseModel):
    team_name: str
class TeamCreate(TeamBase):
    pass
class TeamUpdate(TeamBase):
    pass
class TeamResponse(TeamBase):
    team_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/teams/", response_model=TeamResponse)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    db_team = Team(team_name=team.team_name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team) 
    return db_team

@router.get("/teams/", response_model=List[TeamResponse])
def read_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()

@router.get("/teams/{team_id}", response_model=TeamResponse)
def read_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.team_id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.put("/teams/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, team: TeamUpdate, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.team_id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    db_team.team_name = team.team_name
    db.commit()
    db.refresh(db_team)
    
    return db_team

@router.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.team_id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db.delete(db_team)
    db.commit()
    return {"detail": "Team deleted"}
