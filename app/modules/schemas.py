from pydantic import BaseModel









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
