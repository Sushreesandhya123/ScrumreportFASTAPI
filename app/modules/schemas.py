from pydantic import BaseModel


class SprintProgressBase(BaseModel):
    sprint_id: int
    planned_user_stories: int
    completed_user_stories: int
    incomplete_user_stories: int
    total_team_capacity: int
    planned_story_points: int
    completed_story_points: int
    incomplete_story_points: int
class SprintProgressCreate(SprintProgressBase):
    pass
class SprintProgressUpdate(SprintProgressBase):
    pass
class SprintProgressResponse(SprintProgressBase):
    progress_id: int



class IndividualPerformanceBase(BaseModel):
    sprint_id: int
    member_name: str
    planned_story_points: int
    completed_story_points: int
    incomplete_story_points: int
class IndividualPerformanceCreate(IndividualPerformanceBase):
    pass
class IndividualPerformanceUpdate(IndividualPerformanceBase):
    pass
class IndividualPerformanceResponse(IndividualPerformanceBase):
    performance_id: int


class VelocityBase(BaseModel):
    sprint_id: int
    completed_story_points: int
    average_velocity_per_member: float
    velocity_growth_percentage: float
class VelocityCreate(VelocityBase):
    pass
class VelocityUpdate(VelocityBase):
    pass
class VelocityResponse(VelocityBase):
    velocity_id: int
class BlockerBase(BaseModel):
    sprint_id: int
    description: str
class BlockerCreate(BlockerBase):
    pass
class BlockerUpdate(BlockerBase):
    pass

class BlockerResponse(BlockerBase):
    blocker_id: int


class ProductionPipelineReleaseBase(BaseModel):
    sprint_id: int
    app_name: str
    release_number: str
class ProductionPipelineReleaseCreate(ProductionPipelineReleaseBase):
    pass
class ProductionPipelineReleaseUpdate(ProductionPipelineReleaseBase):
    pass
class ProductionPipelineReleaseResponse(ProductionPipelineReleaseBase):
    release_id: int
    
class Config:
        orm_mode = True
