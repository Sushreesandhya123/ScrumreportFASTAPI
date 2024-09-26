from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Blocker(Base):
    __tablename__ = 'blockers'

    blocker_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sprint_id = Column(Integer, ForeignKey('sprints.sprint_id'), nullable=False)
    description = Column(Text, nullable=False)
    sprint = relationship("Sprint")
