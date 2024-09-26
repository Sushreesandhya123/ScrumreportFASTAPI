from sqlalchemy import Column, Integer, String
from app.database import Base

# Team model
class Team(Base):
    __tablename__ = 'teams'

    team_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    team_name = Column(String(255), nullable=False)