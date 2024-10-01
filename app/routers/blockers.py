from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.blockers import Blocker 
# from app.modules.schemas import BlockerCreate, BlockerUpdate, BlockerResponse
from typing import List
from pydantic import BaseModel
from app.modules.sprint import Sprint

router = APIRouter()

class BlockerBase(BaseModel):
    description: str
class BlockerCreate(BlockerBase):
    pass
class BlockerUpdate(BlockerBase):
    pass

class BlockerResponse(BlockerBase):
    blocker_id: int
    sprint_id: int
class Config:
        orm_mode = True    


def get_latest_sprint_id(db: Session) -> int:
    sprint = db.query(Sprint).order_by(Sprint.sprint_id.desc()).first()
    if sprint is None:
        raise HTTPException(status_code=404, detail="No sprints available")
    return sprint.sprint_id

@router.post("/blockers/", response_model=BlockerResponse)
def create_blocker(blocker: BlockerCreate, db: Session = Depends(get_db)):
    sprint_id = get_latest_sprint_id(db)

    db_blocker = Blocker(**blocker.dict(), sprint_id=sprint_id)
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
    sprint_id = get_latest_sprint_id(db)
    for key, value in blocker.dict().items():
        setattr(db_blocker, key, value)
    db_blocker.sprint_id = sprint_id    
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
