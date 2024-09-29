from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.velocity import Velocity  # Import the Velocity model
from app.modules.schemas import VelocityCreate, VelocityUpdate, VelocityResponse
from typing import List
from app.modules.sprint import Sprint

router = APIRouter()

@router.post("/velocities/", response_model=VelocityResponse)
def create_velocity(velocity: VelocityCreate, db: Session = Depends(get_db)):
    sprint = db.query(Sprint).filter(Sprint.sprint_id == velocity.sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    db_velocity = Velocity(**velocity.dict())
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
    if velocity.sprint_id:
        sprint = db.query(Sprint).filter(Sprint.sprint_id == velocity.sprint_id).first()
        if not sprint:
            raise HTTPException(status_code=404, detail="Sprint not found")
    for key, value in velocity.dict(exclude_unset=True).items():
        setattr(db_velocity, key, value)
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
