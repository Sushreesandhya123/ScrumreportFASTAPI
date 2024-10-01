from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.velocity import Velocity  # Import the Velocity model
# from app.modules.schemas import VelocityCreate, VelocityUpdate, VelocityResponse
from typing import List
from pydantic import BaseModel
from app.modules.sprint import Sprint

router = APIRouter()

class VelocityBase(BaseModel):
    completed_story_points: int
    average_velocity_per_member: float
    velocity_growth_percentage: float
class VelocityCreate(VelocityBase):
    pass
class VelocityUpdate(VelocityBase):
    pass
class VelocityResponse(VelocityBase):
    velocity_id: int
    sprint_id: int
class Config:
        orm_mode = True    


def get_latest_sprint_id(db: Session) -> int:
    sprint = db.query(Sprint).order_by(Sprint.sprint_id.desc()).first()
    if sprint is None:
        raise HTTPException(status_code=404, detail="No sprints available")
    return sprint.sprint_id

@router.post("/velocities/", response_model=VelocityResponse)
def create_velocity(velocity: VelocityCreate, db: Session = Depends(get_db)):
    sprint_id = get_latest_sprint_id(db)

    db_velocity = Velocity(**velocity.dict(), sprint_id=sprint_id)
    db.add(db_velocity)
    db.commit()
    db.refresh(db_velocity)
    return db_velocity

@router.get("/velocities/", response_model=List[VelocityResponse])
def read_velocities(db: Session = Depends(get_db)):
    return db.query(Velocity).all()

@router.get("/velocities/{velocity_id}", response_model=VelocityResponse)
def read_velocity(velocity_id: int, db: Session = Depends(get_db)):
    db_velocity = db.query(Velocity).filter(Velocity.velocity_id == velocity_id).first()
    if db_velocity is None:
        raise HTTPException(status_code=404, detail="Velocity not found")
    return db_velocity

@router.put("/velocities/{velocity_id}", response_model=VelocityResponse)
def update_velocity(velocity_id: int, velocity: VelocityUpdate, db: Session = Depends(get_db)):
    db_velocity = db.query(Velocity).filter(Velocity.velocity_id == velocity_id).first()
    if db_velocity is None:
        raise HTTPException(status_code=404, detail="Velocity not found")
    sprint_id = get_latest_sprint_id(db)
    for key, value in velocity.dict().items():
        setattr(db_velocity, key, value)
    db_velocity.sprint_id = sprint_id     
    db.commit()
    db.refresh(db_velocity)
    return db_velocity

@router.delete("/velocities/{velocity_id}")
def delete_velocity(velocity_id: int, db: Session = Depends(get_db)):
    db_velocity = db.query(Velocity).filter(Velocity.velocity_id == velocity_id).first()
    if db_velocity is None:
        raise HTTPException(status_code=404, detail="Velocity not found")
    db.delete(db_velocity)
    db.commit()
    return {"detail": "Velocity deleted"}
