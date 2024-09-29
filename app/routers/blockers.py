from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.blockers import Blocker 
from app.modules.schemas import BlockerCreate, BlockerUpdate, BlockerResponse
from typing import List
from app.modules.sprint import Sprint

router = APIRouter()


@router.post("/blockers/", response_model=BlockerResponse)
def create_blocker(blocker: BlockerCreate, db: Session = Depends(get_db)):
    sprint = db.query(Sprint).filter(Sprint.sprint_id == Blocker.sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    db_blocker = Blocker(**blocker.dict())
    db.add(db_blocker)
    db.commit()
    db.refresh(db_blocker)
    return db_blocker

@router.get("/blockers/", response_model=List[BlockerResponse])
def read_blockers(db: Session = Depends(get_db)):
    return db.query(Blocker).all()

@router.get("/blockers/{blocker_id}", response_model=BlockerResponse)
def read_blocker(blocker_id: int, db: Session = Depends(get_db)):
    db_blocker = db.query(Blocker).filter(Blocker.blocker_id == blocker_id).first()
    if db_blocker is None:
        raise HTTPException(status_code=404, detail="Blocker not found")
    return db_blocker

@router.put("/blockers/{blocker_id}", response_model=BlockerResponse)
def update_blocker(blocker_id: int, blocker: BlockerUpdate, db: Session = Depends(get_db)):
    db_blocker = db.query(Blocker).filter(Blocker.blocker_id == blocker_id).first()
    if db_blocker is None:
        raise HTTPException(status_code=404, detail="Blocker not found")
    if blocker.sprint_id:
        sprint = db.query(Sprint).filter(Sprint.sprint_id == blocker.sprint_id).first()
        if not sprint:
            raise HTTPException(status_code=404, detail="Sprint not found")
    for key, value in blocker.dict(exclude_unset=True).items():
        setattr(db_blocker, key, value)
    db.commit()
    db.refresh(db_blocker)
    return db_blocker

@router.delete("/blockers/{blocker_id}")
def delete_blocker(blocker_id: int, db: Session = Depends(get_db)):
    db_blocker = db.query(Blocker).filter(Blocker.blocker_id == blocker_id).first()
    if db_blocker is None:
        raise HTTPException(status_code=404, detail="Blocker not found")
    db.delete(db_blocker)
    db.commit()
    return {"detail": "Blocker deleted"}
