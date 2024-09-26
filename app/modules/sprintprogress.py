from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class SprintProgress(Base):
    __tablename__ = 'sprintprogress'

    progress_id = Column(Integer, primary_key=True, autoincrement=True)
    sprint_id = Column(Integer, ForeignKey('sprints.sprint_id'), nullable=False)
    planned_user_stories = Column(Integer, nullable=False)
    completed_user_stories = Column(Integer, nullable=False)
    incomplete_user_stories = Column(Integer, nullable=False)
    total_team_capacity = Column(Integer, nullable=False)
    planned_story_points = Column(Integer, nullable=False)
    completed_story_points = Column(Integer, nullable=False)
    incomplete_story_points = Column(Integer, nullable=False)
