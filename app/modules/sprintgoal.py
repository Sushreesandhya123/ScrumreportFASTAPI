from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# Enum class for the sprint goal status
class StatusEnum(enum.Enum):
    DONE = "Done"
    BACKLOG = "Backlog"
    PENDING = "Pending"
class Sprintgoal(Base):
    __tablename__ = 'sprintgoal'  
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(300))
    status = Column(Enum(StatusEnum), nullable=False)  

    sprint_id = Column(Integer, ForeignKey('sprints.sprint_id'), nullable=False)
    sprint = relationship("Sprint", back_populates="sprintgoals")