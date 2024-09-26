from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class ProductionPipelineRelease(Base):
    __tablename__ = 'production_pipeline_releases'
    release_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sprint_id = Column(Integer, ForeignKey('sprints.sprint_id'), nullable=False)
    app_name = Column(String(255), nullable=False)
    release_number = Column(String(255), nullable=False)
    sprint = relationship("Sprint")
