from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class IndividualPerformance(Base):
    __tablename__ = 'individualperformance'

    performance_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sprint_id = Column(Integer, ForeignKey('sprints.sprint_id'), nullable=False)
    member_name = Column(String(255), nullable=False)
    planned_story_points = Column(Integer, nullable=False)
    completed_story_points = Column(Integer, nullable=False)
    incomplete_story_points = Column(Integer, nullable=False)
    
    sprint = relationship("Sprint", back_populates="individual_performance")
