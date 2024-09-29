from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Sprint(Base):
    __tablename__ = 'sprints'

    sprint_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'), nullable=False)
    sprint_number = Column(Integer, nullable=False)
    sprint_duration = Column(String(255), nullable=False)
    date_of_report = Column(Date, nullable=False)
    scrum_master = Column(String(255), nullable=False)
    team = relationship("Team")
    individual_performance = relationship("IndividualPerformance", back_populates="sprint")
    sprintgoals = relationship("Sprintgoal", back_populates="sprint", cascade="all, delete-orphan")

    