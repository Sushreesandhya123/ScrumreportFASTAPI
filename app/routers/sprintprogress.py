from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
# from app.modules import SprintProgressCreate, SprintProgressUpdate, SprintProgressResponse  # Import Pydantic models
from app.modules.sprintprogress import SprintProgress  # Import SQLAlchemy model
from app.database import get_db
from app.modules.sprint import Sprint
from pydantic import BaseModel

router = APIRouter()

class SprintProgressBase(BaseModel):
    planned_user_stories: int
    completed_user_stories: int
    incomplete_user_stories: int
    total_team_capacity: int
    planned_story_points: int
    completed_story_points: int
    incomplete_story_points: int
class SprintProgressCreate(SprintProgressBase):
    pass
class SprintProgressUpdate(SprintProgressBase):
    pass
class SprintProgressResponse(SprintProgressBase):
    progress_id: int
    sprint_id: int
class Config:
        orm_mode = True    



def get_latest_sprint_id(db: Session) -> int:
    sprint = db.query(Sprint).order_by(Sprint.sprint_id.desc()).first()
    if sprint is None:
        raise HTTPException(status_code=404, detail="No sprints available")
    return sprint.sprint_id


@router.post("/sprintprogress/", response_model=SprintProgressResponse)
def create_sprintprogress(sprintprogress: SprintProgressCreate, db: Session = Depends(get_db)):
    sprint_id = get_latest_sprint_id(db)

    db_sprintprogress = SprintProgress(**sprintprogress.dict(), sprint_id=sprint_id)
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
    sprint_id = get_latest_sprint_id(db)
    for key, value in sprintprogress.dict().items():
        setattr(db_sprintprogress, key, value)
    db_sprintprogress.sprint_id = sprint_id    
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
