from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base

class Velocity(Base):
    __tablename__ = 'velocity'

    velocity_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sprint_id = Column(Integer, ForeignKey('sprints.sprint_id'), nullable=False)
    completed_story_points = Column(Integer, nullable=False)
    average_velocity_per_member = Column(DECIMAL(10, 2), nullable=False)
    velocity_growth_percentage = Column(DECIMAL(5, 2), nullable=False)
    sprint = relationship("Sprint")
